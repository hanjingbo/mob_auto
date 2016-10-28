#coding=utf-8
"""
    desc: 
    input: 
    output:
    name: han
    date: 20160817
    modify:
"""

import sys
import time
import json
sys.path.append('..')
from mob_autotag import search, simrule, word
from util.util import exec_cmd, set_logging_config
reload(sys)
sys.setdefaultencoding('UTF8')

def get_word_dict(word_json, raw_word_json):
    doc_word, raw_doc_word = json.loads(word_json), json.loads(raw_word_json)
    doc_word_dict = {}
    for i,j in doc_word:
        doc_word_dict.setdefault(i, 0.0)
        doc_word_dict[i] += j
    for i,j in raw_doc_word:
        doc_word_dict.setdefault(i, 0.0)
        doc_word_dict[i] += j
    return doc_word_dict

def get_word_from_ad(in_ad):
    print '正在爬取该文案的文本:' + in_ad + "\n"
    doc = search.main_Baidu(in_ad)    

    word_tag2weight = simrule.tag2dict()    
    tag_json, word_json, raw_word_json = \
                    simrule.doc2vect(doc, word_tag2weight)
    outline = [in_ad, tag_json, word_json, raw_word_json, doc]
    vect_ad_file = '../data/rule/vect_ad'
    fwp = open(vect_ad_file, 'a')
    fwp.write("\t".join(outline) + "\n")
    fwp.close
    return tag_json, word_json, raw_word_json

def get_transfor_ad(in_ad, ad_dict, doc_dict):
    in_ad = in_ad.decode('utf-8', "replace")
    mix_dict = {}
    for i in doc_dict:
        if i not in ad_dict: continue
        mix_dict[i] = doc_dict[i]

    mix_sort = sorted(mix_dict.iteritems(), key=lambda d:d[1], reverse = True)[:3]
    print json.dumps(mix_sort, ensure_ascii=False)
    transfor_ad = in_ad
    for i,j in mix_sort:
        trans_str = " [" + i + "] "
        transfor_ad = transfor_ad.replace(i, trans_str)

    return transfor_ad

if __name__ == "__main__":

    in_ad = '联想YOGA平板999元 更多优惠尽在联想粉丝节'
    if len(sys.argv) == 2:
        in_ad = sys.argv[1]
    print '\n' + '原始文案：' + in_ad

    vect_ad_file = '../data/rule/vect_ad'
    ad_vect = {}
    for line in file(vect_ad_file):
        line = line.strip().split("\t")
        if len(line)<4: continue
        rule, tag_vect, word_vect, raw_word_vect = line[:4]
        ad_vect[rule] = [tag_vect, word_vect, raw_word_vect]

    
    doc_word_dict = {}
    word_json, raw_word_json = "",""
    if in_ad in ad_vect:
        tag_json, word_json, raw_word_json = ad_vect[in_ad]
    else:
        tag_json, word_json, raw_word_json = get_word_from_ad(in_ad)
    doc_word_dict = get_word_dict(word_json, raw_word_json)
    doc_word_json = json.dumps(doc_word_dict, ensure_ascii=False)
    #print doc_word_json
    print tag_json

    #print '正在对该文案分词...'
    ad_word_dict = {}
    word.allword_by_pynlpir(in_ad, ad_word_dict)
    ad_word_json = json.dumps(ad_word_dict, ensure_ascii=False)
    #print ad_word_json

    print '\n' + "得到智能文案替换结果:"
    print get_transfor_ad(in_ad, ad_word_dict, doc_word_dict)
