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

    inputfile = "../data/input"
    linkfile = "../data/link"
    link.main(inputfile, linkfile, 1)

    docfile = "../data/doc"
    doc.main(linkfile, docfile, 3, 10)
    
    wordfile = "../data/word"
    word.main(docfile, wordfile, 2000)
