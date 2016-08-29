#coding=utf-8
"""
    desc: get link from source url
    input: file(../data/sql_url_cate)
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
import random
import urllib2
import urlparse
from bs4 import BeautifulSoup
sys.path.append('..')
from util.util import get_user_agent, add_url_header, print_proc_log
reload(sys)
sys.setdefaultencoding('UTF8')


def url_to_link(url, url_key, url_dict):

    url = add_url_header(url)

    if url in url_dict and 'link' in url_dict[url]:
        return ""

    #send_headers = {'User-Agent':'Mozilla/6.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    send_headers = {'User-Agent':get_user_agent()}
    content = ""
    try:
        req = urllib2.Request(url, headers=send_headers)
        content = urllib2.urlopen(req, timeout=10).read()
        content = BeautifulSoup(content, "lxml")
        url_dict.setdefault(url,{})
        url_dict[url].setdefault("link", 1)

    except Exception, e:
        print "exception %s" % str(e) + " link: " + url

    if len(content) == 0:
        return ""
        
    anchors = content.findAll('a')
    for anchor in anchors:
        try:
            if not anchor.has_key('href'):
                continue

            anchor_href = anchor['href']

            if not re.search(url_key, anchor_href):
                continue

            anchor_href = add_url_header(anchor_href)

            if anchor_href not in url_dict:
                url_dict.setdefault(anchor_href,{})

        except Exception, e:
            print "exception %s" % str(e)
            continue


def link_to_link(url_link_dict, url, key, max_cnt=2000):

    url_to_link(url, key, url_link_dict)

    last2len, lastlen, curlen = 0, 0, 0

    # get from link to link
    for i in url_link_dict.keys():
        if 'link' in url_link_dict[i]: continue

        url_to_link(i, key, url_link_dict)
        print "link len:" + str(len(url_link_dict))

        if len(url_link_dict)>max_cnt: break

        # no more add link in 3 times, then break
        curlen = len(url_link_dict)
        if last2len>0 and curlen==last2len: break
        last2len = lastlen
        lastlen = curlen

def link_to_file(url_dict, url, cate, outfile):

    wfd = open(outfile, 'a')
    for i in url_dict.keys():
        wfd.write(i + "\t" + url + "\t" + cate + "\n")
    wfd.close()

def main(inputfile, outfile, max_cnt=2000):
    if os.path.exists(outfile):
        os.remove(outfile)

    sum_cnt = 0
    for line in file(inputfile):
        if line.replace(" ","")[0] == "#": continue
        line = line.strip().split("\t")
        if len(line)<3: continue
        url, key, cate = line[:3]

        url_link_dict = {}
        link_to_link(url_link_dict, url, key, max_cnt=max_cnt)
        link_to_file(url_link_dict, url, cate, outfile)

        sum_cnt += len(url_link_dict)
        print_proc_log("link", sum_cnt, 300)
