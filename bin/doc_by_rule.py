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
from mob_autotag import search, simrule
from util.util import exec_cmd, set_logging_config
reload(sys)
sys.setdefaultencoding('UTF8')

if __name__ == "__main__":

    in_rule = 'app=美丽说'
    if len(sys.argv) == 2:
        in_rule = sys.argv[1]
    
    print '正在爬取该规则的文本:' + in_rule + "\n"
    doc = search.main_Baidu(in_rule)    
    vect_rule_file = '../data/rule/vect_rule'

    rule_type, rule = in_rule.split("=")[:2]
    word_tag2weight = simrule.tag2dict()    
    tag_json, word_json, raw_word_json = \
                    simrule.doc2vect(doc, word_tag2weight)
    outline = [rule, rule_type, tag_json, word_json, raw_word_json, doc]
    fwp = open(vect_rule_file, 'a')
    fwp.write("\t".join(outline) + "\n")
    fwp.close
    print '规则已生成'
