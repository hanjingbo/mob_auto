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
from mob_autotag import simrule
from util.util import exec_cmd, set_logging_config
reload(sys)
sys.setdefaultencoding('UTF8')

if __name__ == "__main__":

    rule = 'app=美丽说'
    rate = 0.5
    fkey = 'rule'
    if len(sys.argv) == 2:
        rule = sys.argv[1]
    if len(sys.argv) == 3:
        rule = sys.argv[1]
        rate = float(sys.argv[2])
    if len(sys.argv) == 4:
        rule = sys.argv[1]
        rate = float(sys.argv[2])
        fkey = sys.argv[3]
    
    print '想推广的项目是:' + rule + "\n"

    print '推荐的相关规则是:'
    simrule.get_rule_sim(rule,rate,fkey)

