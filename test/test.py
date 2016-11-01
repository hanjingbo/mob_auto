#coding=utf-8
import sys
import time
from urlparse import urlparse
sys.path.append('..')
#from mob_autotag import input, link, doc, word, tag
from mob_autotag import word_norm
from util.util import exec_cmd, search_to_fpath


f = "adv_rule"
for line in file(f):
    line = line.strip().split("\t")
    if len(line)<3: continue
    url, cate, w = line[:3]
    domain = urlparse(url).netloc
    print domain+"\t"+cate+"\t"+w

"""
path, filename = '/Users/hanjingbo/git/mob_autotag/data', 'word_'
l = search_to_fpath(path, filename)
if len(l) > 0:
    for i in l:
        postfix = i.split(path+"/"+filename)[1]
        print postfix
        #postfix = '体育运动_'
        word_norm.main(postfix, 100000)
"""

"""
def getword(f):
    #f = '/Users/hanjingbo/MyDataScienceToolbox/word_result/行业词典_IT产品.csv'
    l = []
    for line in file(f):
        line = line.decode('gb2312', "replace").strip().split(",")
        word = line[0].replace('\"','')
        weight = line[2].replace('%','').replace('\"','')
        if word=='关键词': continue
        
        l.append(word + "\t" + weight)
    return l

path, filename = '/Users/hanjingbo/MyDataScienceToolbox/word_result', '行业词典'
l = search_to_fpath(path, filename)
if len(l) > 0:
    for i in l:
        postfix = i.split(path)[1].split(".csv")[0]
        subp = postfix.split("_")
        if len(subp)==2:
            cate, subcate = subp[1], ""
        else:
            cate, subcate = subp[1], subp[2]

        for j in getword(i):
            print "id" + "\t" + j + "\t" + cate + "\t" + subcate
"""
"""
f = '/Users/hanjingbo/MyDataScienceToolbox/word_result'
id2rule = {}
for line in file(f):
    line = line.strip().split("\t")
    if len(line)<3: continue
    app_id, package, id = line[:3]
    id2rule.setdefault(id, [])
    id2rule[id].append(app_id + "," + package)

f = 'map'
for line in file(f):
    line = line.strip().split("\t")
    if len(line)<3: continue
    id_new, name, ids = line[:3]

    if len(ids)<=1: continue
    for id in ids.split(","):
        if id not in id2rule or len(id2rule[id])==0: continue
        for apps in id2rule[id]:
            for app in apps.split(","):
                if len(app)<=1: continue
                print "\t".join([id_new, name, "app_id="+app])
"""
