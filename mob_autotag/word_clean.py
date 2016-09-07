#coding=utf-8
"""
    desc: 
    input: file(../data/result/word)
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
from mob_autotag.word import wordclass_by_pynlpir
reload(sys)
sys.setdefaultencoding('UTF8')

def zscore_norm(x):
    return (x - x.mean())/x.std()

def clean(inputlist, z_min=0.8, std_min=0.03):
    w = np.array(inputlist)
    w_mean = w.mean()
    w_std = w.std()
    w_norm = zscore_norm(w)
    if w_std>std_min:
        w_out = w*(w_norm>z_min)
    else:
        w_out = w*0
    out_list = w_out.tolist()

    return out_list

def main():

    inputfile = "../data/result/word" 
    outfile = "../data/result/clean"
    #inputcate = "3c,jinrong,muying,qiche,lvyou,fang"
    inputcate = "baojian,diannao,fu_,jiaoyu"
    outfile = outfile + "_" + inputcate
    print inputcate

    #for test
    inputfile = "../data/result/test/word"
    outfile = "../data/result/test/clean"
    inputcate = "muying,qiche"

    w2list = {}
    w2dict = {}
    clist = inputcate.split(",")
    if len(clist) > 0:
        for i in clist:
            i = inputfile + "_" + i
            for line in file(i):
                line = line.strip().split("\t")
                if len(line)<4: continue
                cate, word, word_class, weight = line[:4]
                w2dict.setdefault(word, {})
                w2dict[word][cate] = float(weight)

    id2c, c2id = {},{}
    for id in range(len(clist)):
        id2c[id] = clist[id]
        c2id[clist[id]] = id
    c_len = len(clist)

    for w in w2dict:
        if len(w2dict[w]) > c_len-2:
            c_list = [0]*c_len
            for c in w2dict[w]:
                c_list[c2id[c]] = w2dict[w][c]

            w2list.setdefault(w,[])
            w2list[w] = c_list

    wfd = open(outfile, 'w')
    for w in w2list:
        l = w2list[w]
        lc = clean(w2list[w])
        for id in range(len(lc)):
            if l[id]>0 and lc[id]==0:
                wfd.write(id2c[id] + "\t" + w + "\t" + str(l[id]) + "\n")
    wfd.close()
    
if __name__ == "__main__":
    main()
