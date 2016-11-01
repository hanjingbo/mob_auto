#coding=utf-8
import MySQLdb
import pandas as pd
import sys
import json
import re
import time
reload(sys)
sys.setdefaultencoding('UTF8')

def pd_237_category(outfile):
    conn = MySQLdb.connect(host='192.168.144.237', user='data',passwd='PIN239!@#$%^&8', charset='utf8')
    conn.select_db('category')
    sql = """select website, raw_data, keywords from advertiser_vertical_rule where setting_time>='2015-01-01'"""
    df = pd.read_sql(sql=sql, con=conn)
    conn.close()

    with open(outfile, 'w') as f:
        df.to_csv(f, sep="\t", header=False, index=False)


def pd_by_adv_cate(adv_id='5535', cate='手机', outfile='../data/test'):
    conn = MySQLdb.connect(host='192.168.144.12', user='data',passwd='PIN239!@#$%^&8', charset='utf8')
    conn.select_db('optimus')
    sql = "select name, category, brand from product_info where advertiser_id=" + adv_id + " and category like \"%" + cate + "%\""
    url_df = pd.read_sql(sql=sql, con=conn)
    conn.close()

    with open(outfile, 'w') as f:
        url_df.to_csv(f, sep="\t", header=False, index=False)


def pd_12_optimus(outfile='../data/test'):
    conn = MySQLdb.connect(host='192.168.144.12', user='data',passwd='PIN239!@#$%^&8', charset='utf8')
    conn.select_db('optimus')
    sql = "select name, category, brand from product_info where advertiser_id in (7551, 5535, 9348, 3998, 5402, 9351) or pic_url01=5526"
    url_df = pd.read_sql(sql=sql, con=conn)
    conn.close()

    with open(outfile, 'w') as f:
        url_df.to_csv(f, sep="\t", header=False, index=False)


if __name__ == "__main__":
    pd_237_category("adv_rule")    
