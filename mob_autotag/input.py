#coding=utf-8
import MySQLdb
import pandas as pd
import sys
import json
import re
import time
reload(sys)
sys.setdefaultencoding('UTF8')

def rule_new_by_cate(cate, outfile):
    conn = MySQLdb.connect(host='192.168.144.237', user='data',passwd='PIN239!@#$%^&8', charset='utf8')
    conn.select_db('category')
    sql = """select distinct domain, domain, category_list from rule_new where starting_position=0 and category_list=""" + cate
    url_df = pd.read_sql(sql=sql, con=conn)
    conn.close()

    with open(outfile, 'w') as f:
        url_df.to_csv(f, sep="\t", header=False, index=False)



def adv_vertical_by_name(name, outfile):
    conn = MySQLdb.connect(host='192.168.144.237', user='data',passwd='PIN239!@#$%^&8', charset='utf8')
    conn.select_db('category')
    sql = "select website, website, category_id from advertiser_vertical_rule where raw_data like \'%" + name + "%\'"
    url_df = pd.read_sql(sql=sql, con=conn)
    conn.close()

    with open(outfile, 'w') as f:
        url_df.to_csv(f, sep="\t", header=False, index=False)

