#coding=utf-8
"""
    desc: 
    output:
    name: han
    date: 20161025
    modify:
"""

import sys
import thread
import json
import re
import os
import time
sys.path.append('..')
from util.util import exec_cmd, search_to_fpath
from mob_autotag.word import word_by_pynlpir
from mob_autotag.word_norm import norm_from_dict
reload(sys)
sys.setdefaultencoding('UTF8')


def tag2dict():
    tag_path = "../data/result"
    tag_file = "word"
    l = search_to_fpath(tag_path, tag_file)
    tag2id, id2tag, word2id, id2word, word_tag2weight = {}, {}, {}, {}, {}
    for i in l:
        for line in file(i):
            line = line.decode('utf-8', "replace").strip().split("\t")
            tag, word, c, weight = line[:4]
            if tag not in tag2id:
                tag2id[tag] = len(tag2id)
            if word not in word2id:
                word2id[word] = len(word2id)
            word_tag2weight.setdefault(word, {})
            word_tag2weight[word][tag] = float(weight)
    for tag in tag2id:
        _id = tag2id[tag]
        id2tag[_id] = tag
    for word in word2id:
        _id = word2id[word]
        id2word[_id] = word

    return word_tag2weight

def doc2vect(doc, word_tag2weight):
    word_input = {}
    word_by_pynlpir(doc, word_input)
    raw_word_norm = norm_from_dict(word_input,'maxmin')
    raw_word_sort = sorted(raw_word_norm.iteritems(), key=lambda d:d[1], reverse = True)
    raw_word_json = json.dumps(raw_word_sort[:20], ensure_ascii=False)

    tag2score = {}
    word2score = {}
    for word in raw_word_norm:
        if word not in word_tag2weight: continue
        word2score[word] = raw_word_norm[word]
        for tag in word_tag2weight[word]:
            tag2score.setdefault(tag, 0.0)
            tag2score[tag] += word_tag2weight[word][tag]*float(raw_word_norm[word])

    word_sort = sorted(word2score.iteritems(), key=lambda d:d[1], reverse = True)
    word_json = json.dumps(word_sort[:20], ensure_ascii=False)
    tag_sort = sorted(tag2score.iteritems(), key=lambda d:d[1], reverse = True)
    tag_json = json.dumps(tag_sort[:5], ensure_ascii=False)
    
    return tag_json, word_json, raw_word_json


def get_all_vect(fkey="test"):

    inputfile = "../data/rule/doc_" + fkey
    outfile = "../data/rule/vect_tag_" + fkey
    if os.path.exists(outfile):
        os.remove(outfile)
    
    tag2id, id2tag, word2id, id2word, word_tag2weight = {},{},{},{},{}
    word_tag2weight = tag2dict()
    for line in file(inputfile):
        line = line.decode('utf-8', "replace").strip().split("\t")
        if len(line)<2: continue
        rule, doc = line[:2]
        if rule.find('网站')>0:
            rule = rule.replace('网站','')
            rule_type = 'site'
        else:
            rule = rule.replace('app','')
            rule_type = 'app'

        try:
            tag_json, word_json, raw_word_json = \
                doc2vect(doc, word_tag2weight)
            print "\t".join([rule, rule_type, tag_json, word_json, raw_word_json, doc])
        
        except Exception, e:
            print "\n" + "exception_%s" % str(e) + "_" + rule + "_" + doc + "\n"

def get_rule_sim(input_rules, rate=0.5, fkey="test"):
    rate = max(min(rate,0.9999),0.0001)
    infile = "../data/rule/vect_" + fkey
    rule2vect = {}
    for line in file(infile):
        if line.find('pynlpir')>0: continue
        line = line.strip().split("\t")
        if len(line)<5: continue

        rule, rule_type, tag_vect, word_vect, raw_word_vect = line[:5]
        rule_dim = rule_type + "=" + rule
        rule2vect.setdefault(rule_dim,{})
        rule2vect[rule_dim]["tag"] = json.loads(tag_vect)
        rule2vect[rule_dim]["word"] = json.loads(word_vect)
        rule2vect[rule_dim]["raw_word"] = json.loads(raw_word_vect)

    in2dict = {}
    for in_rule in input_rules.split(","):
        if in_rule in rule2vect:
            in2dict[in_rule] = 1
    if len(in2dict)==0:
        """
        说明输入规则可能不在目前模型库中
        可以找相关规则
        """
        corr2dict = {}
        for in_rule in input_rules.split(","):
            for all_rule in rule2vect:
                if in_rule in all_rule or all_rule in in_rule:
                    corr2dict[all_rule] = 1
        if len(corr2dict)>0:
            print '可以尝试如下输入:'
            for i in corr2dict:
                print i
        else:
            """
            说明输入规则可能不在目前模型库中
            可以进行搜索规则入库
            """
            print "python doc_by_rule.py " + in_rule 
        return "null"

    rule2sim = {}
    for r1 in in2dict:
        for r2 in rule2vect:
            v1 = rule2vect[r1]
            v2 = rule2vect[r2]
            v1_list, v2_list = json2list(v1, v2, rate)

            rule2sim.setdefault(r2, 0.0)
            #rule2sim[r2] += 1 - distance(v1_list,v2_list)
            rule2sim[r2] += cos(v1_list,v2_list)

    sim_sort = sorted(rule2sim.iteritems(), key=lambda d:d[1], reverse = True)
    sim_json = json.dumps(sim_sort[:50], ensure_ascii=False)

    print sim_json


def json2list(v1, v2, rate):
    """
    将json列表 统一成编码后的权重列表
    """
    w2id = {}
    out_v1, out_v2 = [], []
    rate2dict = {}
    rate2dict["tag"], rate2dict["word"], rate2dict["raw_word"] = \
        rate, (1-rate)/2.0, (1-rate)/2.0

    # get w2id{}
    for v_type in ["tag", "word", "raw_word"]:
        for word,weight in v1[v_type]:
            if word not in w2id:
                w2id[word] = len(w2id)
        for word,weight in v2[v_type]:
            if word not in w2id:
                w2id[word] = len(w2id)
    # init out_v1, out_v2
    out_v1, out_v2 = [0]*len(w2id), [0]*len(w2id)
    
    # get out_v1, out_v2
    for v_type in ["tag", "word", "raw_word"]:
        for word,weight in v1[v_type]:
            score = weight*rate2dict[v_type]
            out_v1[w2id[word]] += score
        for word,weight in v2[v_type]:
            score = weight*rate2dict[v_type]
            out_v2[w2id[word]] += score
    return out_v1, out_v2

def cos(vector1,vector2):  
    dot_product = 0.0;  
    normA = 0.0;  
    normB = 0.0;  
    for a,b in zip(vector1,vector2):  
        dot_product += a*b  
        normA += a**2  
        normB += b**2  
    if normA == 0.0 or normB==0.0:  
        return None  
    else:  
        return dot_product / ((normA*normB)**0.5)

def distance(vector1,vector2):  
    d=0;  
    for a,b in zip(vector1,vector2):  
        d+=(a-b)**2;  
    return d**0.5;

if __name__ == "__main__":
    fkey = "rule20161025"
    #fkey = "test"
    #get_all_vect(fkey) 

    #get_rule_sim("app=美丽说",0,fkey)
    get_rule_sim("app=美丽说",0.5,fkey)
    #get_rule_sim("app=美丽说",1,fkey)
