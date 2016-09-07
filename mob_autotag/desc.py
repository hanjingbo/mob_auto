#coding=utf-8
"""
    desc: 
    output:
    name: han
    date: 20160818
    modify:
"""

import sys
import thread
import json
import re
import os
import time
from ChineseTone import *
from random import choice
sys.path.append('..')
from util.util import exec_cmd, search_to_fpath
from mob_autotag.word import allclass_by_pynlpir
from mob_autotag.word_norm import norm_from_dict
reload(sys)
sys.setdefaultencoding('UTF8')


def print_and_save(dict, outfile):
    wfd = open(outfile, 'w')
    
    class2score = {}
    class2dict = {}
    class2list = {}
    for dim in dict:
        if len(dim.split("\t")) != 2:
            continue
        _word, _class = dim.split("\t")
        class2dict.setdefault(_class, {})
        class2dict[_class][_word] = dict[dim]
        class2score.setdefault(_class, 0.0)
        class2score[_class] += dict[dim]

    print "\n=============================================="
    print "相关词："
    for _class in class2dict:
        class2list[_class] = sorted(class2dict[_class].iteritems(), key=lambda d:d[1], reverse = True)

    class_sort = sorted(class2score.iteritems(), key=lambda d:d[1], reverse = True)
    for _class, score in class_sort:
        p_str = ""
        for word,weight in class2list[_class][:5]:
            p_str += word + ":" + str(round(weight,2)) + " "
        print _class + "\t" + str(round(score,2)) + "\t[" + p_str + "]"

        for word,weight in class2list[_class]:
            wfd.write(_class + "\t" + str(score) + "\t" + word + "\t" + str(weight) + "\n")
    wfd.close()

def get_toplist(inputlist, topN):
    p_str = ""
    for k,v in inputlist[:topN]:
        p_str += k + ":" + str(round(v,2)) + " "
    return p_str

def get_wordclass(fkey="test", min_word=50):

    inputfile = "../data/doc_" + fkey
    outfile = "../data/desc_" + fkey
    word_input = {}
    f = open(inputfile,'r').read().decode('utf-8', "replace")
    if len(f)< min_word:
        print "document word count is too small, less than " + str(min_word)
        return ""

    allclass_by_pynlpir(f, word_input, 5000)
    word_norm = norm_from_dict(word_input)
    
    print_and_save(word_norm, outfile)


def if_sameyin(word, sentence):
    flag = False
    index = -1
    new_s1, new_s2 = "",""
    word = word.decode('utf-8', "replace")
    sentence = sentence.decode('utf-8', "replace")
    wd_pin = PinyinHelper.convertToPinyinFromSentence(word[-1], pinyinFormat=PinyinFormat.WITHOUT_TONE)[-1]
    st_pinlist = PinyinHelper.convertToPinyinFromSentence(sentence, pinyinFormat=PinyinFormat.WITHOUT_TONE)
    if wd_pin in st_pinlist:
        flag = True
        index = st_pinlist.index(wd_pin)
        new_s1 = sentence[:index] + "(" + word + ")" + sentence[index:]
        new_s2 = sentence[:index] + "\"" + word + "\"" + sentence[index+1:]
    return flag, index, new_s1, new_s2

def if_sameyin_bydict(word, inputdict, yun2list):
    outdict = {}
    outlist = []
    for _word in inputdict:
        flag, index, new_s1, new_s2 = if_sameyin(word, _word)
        if flag:
            outdict[_word] = inputdict[_word]
            """
            yun = get_yun(_word)
            yun2list.setdefault(yun, {})
            yun2list[yun].setdefault(word, {})
            yun2list[yun][word].setdefault(_word, 0.0)
            yun2list[yun][word][_word] = inputdict[_word]
            """
            yun = get_yun(new_s2)
            yun2list.setdefault(yun, {})
            yun2list[yun].setdefault(word, {})
            yun2list[yun][word].setdefault(new_s2, 0.0)
            yun2list[yun][word][new_s2] = inputdict[_word]
    outlist = sorted(outdict.iteritems(), key=lambda d:d[1], reverse = True)
    return outlist

def get_yun(word):
    yun = ""
    try:
        word = word.decode('utf-8', "replace")
        wd_pin = PinyinHelper.convertToPinyinFromSentence(word[-1], pinyinFormat=PinyinFormat.WITHOUT_TONE)[-1]
        wd_sm = PinyinHelper.getShengmu(wd_pin)
        if wd_sm == None:
            yun = wd_pin
        else:
            yun = wd_pin.split(wd_sm)[1]
    except Exception, e:
        print "exception %s" % str(e)+" "+word

    return yun

def if_sameyun(word, sentence):
    flag = False
    word = word.decode('utf-8', "replace")
    sentence = sentence.decode('utf-8', "replace")
    try:
        wd_ym = get_yun(word)
        st_pin = PinyinHelper.convertToPinyinFromSentence(sentence, pinyinFormat=PinyinFormat.WITHOUT_TONE)[-1]
        if st_pin.endswith(wd_ym):
            flag = True
    except Exception, e:
        print "exception %s" % str(e)+" "+word+" "+sentence
    return flag


def if_sameyun_bydict(word, inputdict):
    outdict = {}
    outlist = []
    for _word in inputdict:
        flag = if_sameyun(word, _word)
        if flag:
            outdict[_word] = inputdict[_word]
    outlist = sorted(outdict.iteritems(), key=lambda d:d[1], reverse = True)
    return outlist

def get_related_dict(word_dict, class_dict, inputfile):
    outdict = {}
    for line in file(inputfile):
        line = line.strip().decode('utf-8', "replace")
        s = 0.0
        for w in word_dict:
            if w in line and class_dict[w] in ['noun','verb','adjective']:
                s += word_dict[w]
        outline = line.split("\t")[0]
        if len(outline)<=1 or len(outline)>=20: continue
        outdict[outline] = s
    outlist = sorted(outdict.iteritems(), key=lambda d:d[1], reverse = True)
    return outdict, outlist

def main(query="品友", fkey="test", min_word=50):

    #get_wordclass(fkey, min_word)

    inputfile = "../data/desc_" + fkey
    outfile = "../data/desc_out_" + fkey
    #chengyufile = "../data/chengyu.txt"
    #chengyufile = "../data/chengyu_bao.txt"
    chengyufile = "../data/chengyu_bian.txt"
    gecifile = "../data/geci.txt"

    w2weight = {}
    w2class = {}
    for line in file(inputfile):
        line = line.strip().decode('utf-8', "replace").split("\t")
        if len(line)<4: continue
        c, cw, w, ww = line[:4]
        if c not in ['noun', 'verb', 'adjective']: continue
        w2weight[w] = float(ww)
        w2class[w] = c

    cy_dict, cy_list = get_related_dict(w2weight, w2class, chengyufile)
    #print get_toplist(cy_list, 30)

    #gc_dict, gc_list = get_related_dict(w2weight, w2class, gecifile)
    #print get_toplist(gc_list, 30)

    yin_dict, yun_dict, cy_yin_dict, cy_yun_dict, gc_yin_dict, gc_yun_dict = {},{},{},{},{},{}
    query = query.decode('utf-8', "replace")
    for word in query:
        #yin_dict[word] = if_sameyin_bydict(word, w2weight, yun_dict)
        cy_yin_dict[word] = if_sameyin_bydict(word, cy_dict, cy_yun_dict)
        #gc_yin_dict[word] = if_sameyin_bydict(word, gc_dict, gc_yun_dict)

    """
    for yun in yun_dict:
        for word in yun_dict[yun]:
            print yun, word, choice(yun_dict[yun][word].keys())
    """

    s_dict = {}
    for yun in cy_yun_dict:
        if len(cy_yun_dict[yun])<1: continue
        for i in range(10):
            s = ""
            for word in query:
                if word not in cy_yun_dict[yun]: continue
                rand_w = choice(cy_yun_dict[yun][word].keys())
                if len(rand_w) > 7: continue
                if len(rand_w) != 0:
                    s += rand_w + "\t"
            #if len(s.split(" ")) == 2:
            s_dict[s] = 1

    for j in s_dict:
        if len(j.split("\t")) == 3:
            print j

    """
    for yun in gc_yun_dict:
        for word in gc_yun_dict[yun]:
            print yun, word, choice(gc_yun_dict[yun][word].keys())
    """
    """
        union_yin_list = list(set(yin_dict[word]).union(set(cy_yin_dict[word])).union(set(gc_yin_dict[word])))
        union_yun_list = list(set(yun_dict[word]).union(set(cy_yun_dict[word])).union(set(gc_yun_dict[word])))
        out_dict[word] = list(set(union_yin_list).union(set(union_yun_list))^(set(union_yin_list)^set(union_yun_list)))
        
        print word, get_toplist(out_dict[word], 30)
        print word, "yin", get_toplist(yin_dict[word], 30)
        print word, "yun", get_toplist(yun_dict[word], 30)
        print word, "cy_yin", get_toplist(cy_yin_dict[word], 30)
        print word, "cy_yun", get_toplist(cy_yun_dict[word], 30)
        print word, "gc_yin", get_toplist(gc_yin_dict[word], 30)
        print word, "gc_yun", get_toplist(gc_yun_dict[word], 30)
   """

if __name__ == "__main__":

    cate = "品友"
    if len(sys.argv) >= 2:
        cate = sys.argv[1]
    print cate

    main(cate)
