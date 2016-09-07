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
from mob_autotag import word_norm
from util.util import exec_cmd, set_logging_config
reload(sys)
sys.setdefaultencoding('UTF8')

if __name__ == "__main__":

    fkey = '3c'
    max_words = 3000
    if len(sys.argv) == 3:
        fkey = sys.argv[1]
        max_words = int(sys.argv[2])
    print fkey,max_words

    word_norm.main(fkey, max_words)
