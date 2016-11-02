#coding=utf-8
"""
    desc: 
    input: 
    output:
    name: han
    date: 20160817
    modify:
"""
import MySQLdb
import pandas as pd
import sys
import time
sys.path.append('..')
from mob_autotag import simrule
from util.util import exec_cmd, set_logging_config
reload(sys)
sys.setdefaultencoding('UTF8')

def get_smart_profile():
    conn = MySQLdb.connect(host='192.168.144.237', user='mixdata_insert',passwd='datagroup', charset='utf8')
    conn.select_db('mixdata')
    sql = """select id,word from smart_profile where flag=1 and status=1"""
    df = pd.read_sql(sql=sql, con=conn)
    conn.close()

    word_li = df.to_dict(orient='list')['word']
    id_li = df.to_dict(orient='list')['id']
    id2word = {}
    for i in range(len(id_li)):
        id2word[id_li[i]] = word_li[i]
    return id2word

def update_status(i, s):
    conn = MySQLdb.connect(host='192.168.144.237', user='mixdata_all',passwd='atadxim_datagroup', charset='utf8')
    conn.select_db('mixdata')
    cur = conn.cursor()
    cur.execute("update smart_profile set status=" + s + " where id=" + i)
    cur.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":

    fkey = 'rule'
    in_dict =  get_smart_profile()
    for i in in_dict:
        update_status(str(i),'2')
        for rate in [0.9, 0.5, 0.1]:
            rule = in_dict[i]
            print '想推广的项目是:' + rule + "\n"

            print '推荐的相关规则是:'
            simrule.get_rule_sim(rule,rate,fkey,0.2,5000)

        update_status(str(i),'3')
