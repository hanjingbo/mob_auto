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
from mob_autotag import input, link, doc, word
from util.util import exec_cmd, set_logging_config
reload(sys)
sys.setdefaultencoding('UTF8')

if __name__ == "__main__":

    fkey = '3c'
    inputfile = "../data/input" + "_" + fkey
    linkfile = "../data/link" + "_" + fkey
    link.main(inputfile, linkfile, 1)

    docfile = "../data/doc" + "_" + fkey
    doc.main(linkfile, docfile, 3, 10)
    
    wordfile = "../data/word" + "_" + fkey
    word.main(docfile, wordfile, 2000)
