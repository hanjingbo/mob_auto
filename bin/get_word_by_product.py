#coding=utf-8
"""
    desc: 
    input: 
    output:
    name: han
    date: 20160817
    modify:
"""

import sys
import time
sys.path.append('..')
from mob_autotag import doc, word
from util.util import exec_cmd, set_logging_config
reload(sys)
sys.setdefaultencoding('UTF8')

if __name__ == "__main__":

    fkey = 'test' 
    docfile = "../data/doc" + "_" + fkey
    #doc.pd_by_adv_cate('5535', '手机', docfile)
    doc.doc_by_product_file('电池', docfile, '../data/doc_3c_productaa')

    wordfile = "../data/word" + "_" + fkey
    #word.split_main(docfile, wordfile, 1000)
