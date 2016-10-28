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
from multiprocessing.pool import Pool
from multiprocessing import Queue
import urllib2
import urlparse
from bs4 import BeautifulSoup
sys.path.append('..')
from util.util import exec_cmd, search_to_fpath
from mob_autotag.word import word_by_pynlpir, allclass_by_pynlpir
from mob_autotag.word_norm import norm_from_dict
reload(sys)
sys.setdefaultencoding('UTF8')


def print_and_save(dict, outfile):
    wfd = open(outfile, 'w')
    
    tag2score = {}
    tag2list = {}
    for tag in dict:
        for word in dict[tag]:
            tag2score.setdefault(tag,0.0)
            tag2score[tag] += dict[tag][word]

        tag2list[tag] = sorted(dict[tag].iteritems(), key=lambda d:d[1], reverse = True)

    tagsort = sorted(tag2score.iteritems(), key=lambda d:d[1], reverse = True)
    for tag, score in tagsort:
        if tagsort.index((tag, score)) == 0:
            print "\n=============================================="
            print "机器智能标签为："
        if tagsort.index((tag, score)) == 1:
            print "\n\n=============================================="
            print "其它相似标签为："

        if tagsort.index((tag, score)) >= 1:
            score = score/2
        p_str = ""
        for word,weight in tag2list[tag][:5]:
            p_str += word + ":" + str(round(weight,2)) + " "
        print tag + "\t" + str(round(score,2)) + "\t[" + p_str + "]"

        for word,weight in tag2list[tag]:
            wfd.write(tag + "\t" + str(score) + "\t" + word + "\t" + str(weight) + "\n")
    wfd.close()

def main(fkey="test", min_word=50):

    inputfile = "../data/doc_" + fkey
    outfile = "../data/tag_" + fkey
    wordpath = "../data/result/word"
    cleanfile = "../data/result/clean"
    word_clean = {}
    for line in file(cleanfile):
        line = line.decode('utf-8', "replace").strip().split("\t")
        if len(line)<3: continue
        tag, word, weight = line[:3]
        k = tag + "\t" + word
        word_clean[k] = 1

    word_input = {}
    f = open(inputfile,'r').read().decode('utf-8', "replace")
    if len(f)< min_word:
        print "document word count is too small, less than " + str(min_word)
        return ""

    #word_by_pynlpir(f, word_input)
    allclass_by_pynlpir(f, word_input)
    word_norm = norm_from_dict(word_input)
    wordfile = "../data/word_" + fkey
    save_word(word_norm, wordfile)

    path = os.path.dirname(wordpath)
    filename = os.path.basename(wordpath)

    l = search_to_fpath(path, filename)
    tag_word = {}
    for i in l:
        for line in file(i):
            line = line.decode('utf-8', "replace").strip().split("\t")
            if len(line)<4: continue
            tag, word, word_class, weight = line[:4]

            k = tag + "\t" + word
            if k in word_clean: continue
            if word not in word_norm : continue
            tag_word.setdefault(tag, {})
            tag_word[tag].setdefault(word, 0.0)
            tag_word[tag][word] += float(weight)*word_norm[word]

    print_and_save(tag_word, outfile)

def save_word(word_dict, outfile):
    wfd = open(outfile, 'w')
    word_sort = sorted(word_dict.iteritems(), key=lambda d:d[1], reverse = True)
    for word,weight in word_sort:
        wfd.write(word + "\t" + str(weight) + "\n")
    wfd.close()

if __name__ == "__main__":
    main()
