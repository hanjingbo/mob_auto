#coding=utf-8
import MySQLdb
import pandas as pd
import sys
import json
import re
import time
reload(sys)
sys.setdefaultencoding('UTF8')

def pd_237_category(cate, outfile):
    conn = MySQLdb.connect(host='192.168.144.237', user='data',passwd='PIN239!@#$%^&8', charset='utf8')
    conn.select_db('category')
    sql = """select distinct domain, domain, category_list from rule_new where starting_position=0 and category_list=""" + cate + "limit 10"
    url_df = pd.read_sql(sql=sql, con=conn)
    conn.close()

    with open(outfile, 'w') as f:
        url_df.to_csv(f, sep="\t", header=False, index=False)


def pd_by_adv_cate(adv_id='5535', cate='手机', outfile='../data/test'):
    conn = MySQLdb.connect(host='192.168.144.12', user='data',passwd='PIN239!@#$%^&8', charset='utf8')
    conn.select_db('optimus')
    sql = "select name, category, brand from product_info where advertiser_id=" + adv_id + " and category like \"%" + cate + "%\""
    url_df = pd.read_sql(sql=sql, con=conn)
    conn.close()

    with open(outfile, 'w') as f:
        url_df.to_csv(f, sep="\t", header=False, index=False)

