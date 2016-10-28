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
from mob_autotag import input, link, doc, word, tag, tag_v1
from util.util import exec_cmd, set_logging_config, shuf_sample
reload(sys)
sys.setdefaultencoding('UTF8')

if __name__ == "__main__":

    url = 'http://toutiao.com/a6324190019138404609'
    if len(sys.argv) == 2:
        url = sys.argv[1]
    print url
    fkey = "tmp"

    inputfile = "../data/input_" + fkey
    fwd = open(inputfile, 'w')
    fwd.write(url + "\t" + "url" + "\t" + fkey)
    fwd.close()

    link.main(fkey, 50)
    linkfile = "../data/link_" + fkey

    for i in 10,30,100:
        print "\n正在智能分析" + str(i) + "个网页........"
        shuf_sample(linkfile,i)
        _fkey = fkey + str(i)

        doc.main(_fkey, 3, 3)
        tag.main(_fkey)


