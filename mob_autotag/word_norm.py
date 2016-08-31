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


def main(cate="3c", max_words=3000):

    inputfile = "../data/word_" + cate
    outfile = "../data/result/word_" + cate
    if os.path.exists(outfile):
        os.remove(outfile)

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

    wordlist, weightlist = [], []
    for i,j in outlist:
        wordlist.append(i)
        weightlist.append(j)

    w = np.array(weightlist)
    w_norm = (w - w.min(0)) / w.ptp(0)
    w_normlist = w_norm.tolist()

    wfd = open(outfile, 'w')
    for i in range(len(w_normlist)):
        word, weight = wordlist[i], w_normlist[i]
        wfd.write(cate + "\t" + word + "\t" + str(weight) + "\n")
    wfd.close()


if __name__ == "__main__":
    main()
