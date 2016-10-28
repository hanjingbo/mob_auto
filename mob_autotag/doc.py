#coding=utf-8
"""
    desc: get document from url
    input: file(../data/link)
    output:
    name: han
    date: 20160817
    modify:
"""
import MySQLdb
import pandas as pd
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
                exec_cmd, shuf, search_to_fpath
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


def main_to_file(inputfile, outfile, max_word=3, max_sentence=3):
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
        if cnt<max_sentence:
            doc = ""

        if len(doc)>0:
            wfd = open(outfile, 'a')
            wfd.write(link + "\t" + doc + "\n")
            wfd.close()
            sum_cnt += 1

        print_proc_log("doc", sum_cnt, 500)

def main(fkey, max_word=3, max_sentence=3):
    inputfile = "../data/link_" + fkey
    outfile = "../data/doc_" + fkey
    main_to_file(inputfile, outfile, max_word=max_word, max_sentence=max_sentence)

def doc_by_pd_adv(adv_id='5535', cate='手机', outfile='../data/test'):
    conn = MySQLdb.connect(host='192.168.144.12', user='data',passwd='PIN239!@#$%^&8', charset='utf8')
    conn.select_db('optimus')
    sql = "select name, category, brand from product_info where advertiser_id=" + adv_id + " and category like \"%" + cate + "%\""
    url_df = pd.read_sql(sql=sql, con=conn)
    conn.close()

    with open(outfile, 'w') as f:
        url_df.to_csv(f, sep="\t", header=False, index=False)

def doc_by_product_file(cate="手机", outfile='../data/test', inputfile="../data/doc_all_product"):
    path = os.path.dirname(inputfile)
    filename = os.path.basename(inputfile)

    l = search_to_fpath(path, filename)
    if len(l) > 0:
        wfd = open(outfile, 'w')
        for i in l:
            for line in file(i):
                if cate in line:
                    wfd.write(line)
        wfd.close()



