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
from mob_autotag import doc, word, tag
from util.util import exec_cmd, set_logging_config
reload(sys)
sys.setdefaultencoding('UTF8')

if __name__ == "__main__":

    cate = '电池'
    if len(sys.argv) == 2:
        cate = sys.argv[1]
    print cate

    fkey = "tmp"
    docfile = "../data/doc" + "_" + fkey
    #doc.pd_by_adv_cate('5535', '手机', docfile)
    doc.doc_by_product_file(cate, docfile, '../data/doc_all_product')

    tag.doc_to_tag(docfile, fkey)
