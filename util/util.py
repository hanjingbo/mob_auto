#coding=utf-8
import sys
import thread
import json
import re
import os
import time
import random
import logging
import json
import commands
import subprocess
reload(sys)
sys.setdefaultencoding('UTF8')


def add_url_header(url):
    '''
    if url not have header, add 'http://' to it
    else return it

    '''
    if not re.match('(?:http|ftp|https)://', url):
        url = "http://" + url
    return url

def get_user_agent():
    fp = open('../data/user_agents', 'r')
    user_agents = []
    line  = fp.readline().strip('\n')
    while(line):
        user_agents.append(line)
        line = fp.readline().strip('\n')
    fp.close()

    length = len(user_agents)
    index = random.randint(0, length-1)
    user_agent = user_agents[index]
    return user_agent

def print_proc_log(desc, cnt, scale):
    if cnt%scale == 0:
        print "..." + desc + ":" + str(cnt)

def reg_exp(i):
    return re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\+\-\"\_\ \t\r]", "", i)


def exec_cmd(*cmd_list):
    '''
    execute bash cmd
    '''
    cmd = ' '.join(cmd_list)
    logging.info("executing cmd : " + cmd)
    print cmd
    try :
        exec_output = subprocess.check_output(cmd, shell=True,
                                          stderr=subprocess.STDOUT)

    except subprocess.CalledProcessError, exec_err:
        logging.error("exec cmd : " + str(exec_err.cmd))
        logging.error("return code : " + str(exec_err.returncode))
        logging.error("output : " + str(exec_err.output))


    logging.info("output is : " + exec_output)
    logging.info("finished cmd : " + cmd)

    return exec_output

def set_logging_config(log_file='run.log', mode='w'):
    '''
    set logging format and level
    '''
    logging.basicConfig(level=logging.DEBUG,
                        format ='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        filename = log_file,
                        filemode = mode)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info("output log both screen and " + log_file)


def search_to_file(path, s):
    l = []
    for x in os.listdir(path):
        fp = os.path.join(path, x)
        if os.path.isfile(fp) and  s in x:
            l.append(x)
    return l


def search_to_fpath(path, s):
    l = []
    for x in os.listdir(path):
        fp = os.path.join(path, x)
        if os.path.isfile(fp) and  s in x:
            l.append(fp)
    return l

def shuf(infile, outfile):
    with open(infile, 'r') as f:
        flist = f.readlines()
        random.shuffle(flist)

    fwp = open(outfile, 'w')
    for line in flist:
        fwp.write(line)
    fwp.close()

def shuf_sample(infile, cnt):
    outfile = infile + str(cnt)
    with open(infile, 'r') as f:
        flist = f.readlines()
        random.shuffle(flist)

    if len(flist) < int(cnt): 
        cnt = len(flist)
    fwp = open(outfile, 'w')
    for line in flist[:int(cnt)]:
        fwp.write(line)
    fwp.close()
