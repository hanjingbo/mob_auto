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
    result = (x - min(x)) / (max(x) - min(x) + 0.0001) + 0.1
    return result

def zscore_norm(x):
    return (x - x.mean())/x.std() 

def norm_from_list(_list, func='zscore'):
    wordlist, weightlist, _outlist = [], [], []
    for i,j in _list:
        wordlist.append(i)
        weightlist.append(j)

    w = np.array(weightlist)

    if func=='zscore':
        w_norm = zscore_norm(w)
    elif func=='maxmin':
        w_norm = maxmin_norm(w)

    w_normlist = w_norm.tolist()
    
    for i in range(len(w_normlist)):
        _outlist.append((wordlist[i], w_normlist[i]))
    return _outlist

def norm_from_dict(_dict, func='zscore'):
    _list = sorted(_dict.iteritems(), key=lambda d:d[1], reverse = True)
    _outlist = norm_from_list(_list, func)

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
            _word2dict = {}
            for line in file(i):
                line = line.decode('utf-8', "replace").strip().split("\t")
                if len(line)<3: continue
                word, word_class, weight = line[:3]
                dim = word + "\t" + word_class
                _word2dict.setdefault(dim, 0.0)
                try:
                    _word2dict[dim] += float(weight)
                except Exception, e:
                    print "exception %s" % str(e) + " " + dim + " " + str(weight)

            _word2norm = norm_from_dict(_word2dict,'maxmin')
            for word, weight in _word2norm.iteritems():
                word2dict.setdefault(word, 0.0)
                word2dict[word] += float(weight)

    outlist = sorted(word2dict.iteritems(), key=lambda d:d[1], reverse = True)
    outlist = outlist[:max_words]

    normlist = norm_from_list(outlist, 'maxmin')    

    wfd = open(outfile, 'w')
    for word, weight in normlist:
        wfd.write(cate + "\t" + word + "\t" + str(weight) + "\n")
    wfd.close()


if __name__ == "__main__":
    main()
