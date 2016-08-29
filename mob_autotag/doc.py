#coding=utf-8
"""
    desc: get document from url
    input: file(../data/all_urllink_cate)
    output:
    name: han
    date: 20160817
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
from util.util import get_user_agent, add_url_header, print_proc_log, reg_exp, \
                exec_cmd, shuf
reload(sys)
sys.setdefaultencoding('UTF8')


def url_to_doc(url):

    doc = ""
    url = add_url_header(url)
    send_headers = {'User-Agent':get_user_agent()}
    try:
        req = urllib2.Request(url, headers=send_headers)
        content = urllib2.urlopen(req, timeout=10).read()
        content = BeautifulSoup(content, "lxml")
        body = content.body.get_text()
        doc = reg_exp(body)

    except Exception, e:
        print "exception %s" % str(e)+" doc: "+url

    return doc


def main(inputfile, outfile, max_word=80, max_sentence=3):
    if os.path.exists(outfile):
        os.remove(outfile)

    inputshuf = inputfile + "_shuf"
    shuf(inputfile, inputshuf)
    sum_cnt = 0
    for line in file(inputshuf):
        line = line.strip().split("\t")
        if len(line)<3: continue
        link, url, cate = line[:3]

        raw_doc = url_to_doc(link)
        doc = ""
        cnt = 0
        for i in raw_doc.strip().split("\n"):
            if len(i)>max_word:
                doc += " " + i
                cnt += 1
                #print str(len(i)) + ":" + i
        if cnt<max_sentence:
            doc = ""
        #else:
        #    print str(cnt) + ":" + doc

        if len(doc)>0:
            wfd = open(outfile, 'a')
            wfd.write(url + "\t" + doc + "\n")
            wfd.close()
            sum_cnt += 1

        print_proc_log("doc", sum_cnt, 500)

"""
def split_main(inputfile, outfile, max_word=80, max_sentence=3):
    # remove input_part
    l = search_to_fpath(inputfile)
    l.remove(inputfile)
    if len(l) > 0:
        for i in l:
            os.remove(i)

    suff(inputfile)
    split(inputfile)

    l = search_to_fpath(inputfile)
    l.remove(inputfile)
    if len(l) > 0:
        for i in l:
            postfix = i.split(inputfile)[1]
            o = outfile + postfix
            main(i, o, max_word=max_word, max_sentence=max_sentence)

"""
