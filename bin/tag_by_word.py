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
from mob_autotag import doc, word, tag, search
from util.util import exec_cmd, set_logging_config
reload(sys)
sys.setdefaultencoding('UTF8')

if __name__ == "__main__":

    cate = '电池'
    fkey = "tmp"
    if len(sys.argv) == 2:
        cate = sys.argv[1]
    print cate

    print "\n正在基础智能分析........"
    docfile = "../data/doc" + "_" + fkey
    #doc.pd_by_adv_cate('5535', '手机', docfile)
    doc.doc_by_product_file(cate, docfile, '../data/doc_all_product')
    tag.main(fkey)

    print "\n正在实时爬虫今日头条媒体，进行智能分析........"
    fkey = fkey + "TD"
    docfile = "../data/doc" + "_" + fkey
    search.main_TD(cate,fkey)
    tag.main(fkey)

    print "\n正在实时爬虫google搜索，进行智能分析........"
    fkey = fkey + "GG"
    docfile = "../data/doc" + "_" + fkey
    search.main_GG(cate,fkey)
    tag.main(fkey)
    
