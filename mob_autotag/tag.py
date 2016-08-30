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
from mob_autotag.word import word_by_pynlpir
reload(sys)
sys.setdefaultencoding('UTF8')


def print_and_save(dict, outfile):
    wfd = open(outfile, 'w')
    
    i2w = {}
    for i in dict:
        for j in dict[i]:
            i2w.setdefault(i,0.0)
            i2w[i] += dict[i][j]

        dict[i] = sorted(dict[i].iteritems(), key=lambda d:d[1], reverse = True)

        p_str = ""
        for j,w in dict[i][:5]:
            p_str += j + ":" + str(round(w,2)) + " "
        print i + "\t" + str(round(i2w[i],2)) + "\t[" + p_str + "]"

        for j,w in dict[i]:
            wfd.write(i + "\t" + str(i2w[i]) + "\t" + j + "\t" + str(w) + "\n")

def doc_to_tag(doc="../data/doc", outfile="../data/tag_test", wordpath="../data/result/word"):
    word_input = {}
    f = open(doc,'r').read().decode('utf-8', "replace")
    word_by_pynlpir(f, word_input)

    path = os.path.dirname(wordpath)
    filename = os.path.basename(wordpath)

    l = search_to_fpath(path, filename)
    tag_word = {}
    for i in l:
        for line in file(i):
            line = line.decode('utf-8', "replace").strip().split("\t")
            if len(line)<4: continue
            tag, word, word_class, weight = line[:4]

            dim = word + "\t" + word_class
            if dim not in word_input : continue
            tag_word.setdefault(tag, {})
            tag_word[tag].setdefault(word, 0.0)
            tag_word[tag][word] += float(weight)*word_input[dim]

    print_and_save(tag_word, outfile)


if __name__ == "__main__":
    doc_to_tag()
