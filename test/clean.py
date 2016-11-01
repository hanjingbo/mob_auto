#coding=utf-8

import sys
import re
reload(sys)
sys.setdefaultencoding('UTF8')

wfd = open("chengyu_bao_1.txt",'w')
f = "chengyu_bao.txt"
#f = "test"
for line in file(f):
    line = unicode(line, errors='ignore')
    l = line.replace("\t"," ").replace("，"," ").replace("；"," ").replace("。"," ").replace("\n"," ").replace(u'\u3000'," ").replace(u'\u2028'," ").replace(u'\xa0'," ").split(" ")

    for s in l:
        s = re.sub("[A-Za-z0-9\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\+\-\"\_\ \［\］\r\、\《\》\（\‘\’\）]", "", s)
        s = s.decode('utf-8', "replace")
        if len(s)==4:
            wfd.write(s + "\n")
"""


wfd = open("chengyu.txt",'w')
f = "../data/chengyu.txt"

for line in file(f):
    l = line.strip().decode('utf-8', "replace").replace(" ","").replace("\t","")
    if len(l)==0 and ('拼音' not in l or '释义' not in l): continue
    try:
        chengyu = l.split('拼音')[0]
        shiyi = l.split('释义')[1]
        wfd.write(chengyu + "\t" + shiyi + "\n")
    except Exception, e:
        print "exception %s" % str(e) + l
        
"""
