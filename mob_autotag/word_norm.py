#coding=utf-8
"""
    desc: 
    input: file(../data/word)
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
import numpy as np
sys.path.append('..')
from util.util import exec_cmd, search_to_fpath
reload(sys)
sys.setdefaultencoding('UTF8')

def maxmin_norm(x):
    return (x - x.min(0)) / x.ptp(0)

def zscore_norm(x):
    return (x - x.mean())/x.std()

def norm_from_list(_list):
    wordlist, weightlist, _outlist = [], [], []
    for i,j in _list:
        wordlist.append(i)
        weightlist.append(j)

    w = np.array(weightlist)
    w_norm = zscore_norm(w)
    w_normlist = w_norm.tolist()
    
    for i in range(len(w_normlist)):
        _outlist.append((wordlist[i], w_normlist[i]))
    return _outlist

def norm_from_dict(_dict):
    _list = sorted(_dict.iteritems(), key=lambda d:d[1], reverse = True)
    _outlist = norm_from_list(_list)

    _outdict = {}
    for i,j in _outlist:
        _outdict[i] = j
    return _outdict

def main(cate="3c", max_words=3000):

    inputfile = "../data/word_" + cate
    outfile = "../data/result/word_" + cate

    path = os.path.dirname(inputfile)
    filename = os.path.basename(inputfile)
    l = search_to_fpath(path, filename)
    if len(l) > 0:
        word2dict = {}    
        for i in l:
            for line in file(i):
                line = line.decode('utf-8', "replace").strip().split("\t")
                if len(line)<3: continue
                word, word_class, weight = line[:3]
                dim = word + "\t" + word_class
                word2dict.setdefault(dim, 0.0)
                word2dict[dim] += float(weight)

    outlist = sorted(word2dict.iteritems(), key=lambda d:d[1], reverse = True)
    outlist = outlist[:max_words]

    normlist = norm_from_list(outlist)    

    wfd = open(outfile, 'w')
    for word, weight in normlist:
        wfd.write(cate + "\t" + word + "\t" + str(weight) + "\n")
    wfd.close()


if __name__ == "__main__":
    main()
