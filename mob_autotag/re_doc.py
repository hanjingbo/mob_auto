#coding=utf-8
"""
    desc: 
    input:
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


#TODO: 针对历史爬虫语料，结合当前词包，再次进行语料精选过滤
