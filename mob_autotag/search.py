#coding=utf-8
import os
from os.path import isfile, join
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
import urllib2, socket, time
import gzip, StringIO
import re, random, types
import requests
import json
sys.path.append('..')
from util.util import get_user_agent
from bs4 import BeautifulSoup

class SearchToutiao(object):

    def __init__(self, keywords, count=20, offset=0, search_limit=20):
        self.keywords = keywords
        self.count = count
        self.offset = offset
        self.search_limit = search_limit
        self.search_res_list = []
        self.search_doc_list = []
        self.search_url_list = []
        self.search_image_list = []

    def search_keyword(self):
        base_api = "http://toutiao.com/search_content/?offset={offset}&format=json&keyword={keywords}&autoload=true&count={count}"

        api_url = base_api.format(offset=self.offset,
                                  keywords=self.keywords,
                                  count=self.count)
        headers = {'User-Agent':get_user_agent()}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        ret_html = ""
        res_list = []

        try:
            ret = requests.get(api_url, headers=headers)
            ret_html = ret.text
            ret_json = json.loads(ret_html)
            res_list = ret_json['data']

            while ret_json["has_more"] == 1 and len(res_list) < self.search_limit:
                self.offset += self.count
                api_url = base_api.format(offset=self.offset,
                                          keywords=self.keywords,
                                          count=self.count)
                ret = requests.get(api_url, headers=headers)
                ret_html = ret.text
                ret_json = json.loads(ret_html)
                res_list += ret_json['data']

        except ValueError, ve:
            print ("html return %s" % ret_html)

        except Exception, e:
            print ("html return %s" % ret_html)
            print ("exception type: %s" %  type(e))
            print ("exception during search : %s ") % str(e)

        return res_list

    def get_search_res(self):
        res_list = self.search_keyword()

        for item in res_list:
            title = item['title']
            url = item['url']
            #media_name = item['media_name']
            abstract = item['abstract']
            keywords = item['keywords']
            image_list = item['image_list']
            #media_url = item['media_url']
            article_url = item['article_url']
            display_url = item['display_url']

            self.search_res_list.append({"title": title,
                                         "url": url})
            doc = title + " " + abstract + " " + keywords
            self.search_doc_list.append(doc)
            self.search_url_list.append(url)
            self.search_image_list.append(image_list)

        return self.search_res_list,self.search_doc_list,self.search_url_list,self.search_image_list


class Google:
    # search web
    # @param query -> query key words
    # @param lang -> language of search results
    # @param num -> number of search results to return
    def __init__(self, query, lang='zh', num=30):
        timeout = 40
        socket.setdefaulttimeout(timeout)
        self.query = query
        self.lang = lang
        self.num = num
        self.results_per_page = 10
        self.base_url = 'https://www.google.com.hk/'
        self.search_doc_list = []
        self.search_url_list = []

    def randomSleep(self):
        sleeptime =  random.randint(60, 120)
        time.sleep(sleeptime)

    #extract the domain of a url
    def extractDomain(self, url):
        domain = ''
        pattern = re.compile(r'http[s]?://([^/]+)/', re.U | re.M)
        url_match = pattern.search(url)
        if(url_match and url_match.lastindex > 0):
            domain = url_match.group(1)

        return domain

    #extract a url from a link
    def extractUrl(self, href):
        url = ''
        pattern = re.compile(r'(http[s]?://[^&]+)&', re.U | re.M)
        url_match = pattern.search(href)
        if(url_match and url_match.lastindex > 0):
            url = url_match.group(1)

        return url

    # extract serach results list from downloaded html file
    def extractSearchResults(self, html):
        url_list, doc_list = [], []
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find('div', id  = 'search')
        if (type(div) != types.NoneType):
            lis = div.findAll('div', {'class': 'g'})
            if(len(lis) > 0):
                for li in lis:
                    h3 = li.find('h3', {'class': 'r'})
                    if(type(h3) == types.NoneType):
                        continue

                    # extract domain and title from h3 object
                    link = li.find('a')
                    if (type(link) == types.NoneType):
                        continue

                    url = link['href']
                    url = self.extractUrl(url)
                    if(cmp(url, '') == 0):
                        continue
                    title = link.renderContents()
                    content = li.text

                    self.search_url_list.append(url)
                    doc = title + " " + content
                    self.search_doc_list.append(doc)

    def search(self):
        query = urllib2.quote(self.query)
        results_per_page = self.results_per_page
        num = self.num
        base_url = self.base_url
        if(num % results_per_page == 0):
            pages = num / results_per_page
        else:
            pages = num / results_per_page + 1

        for p in range(0, pages):
            start = p * results_per_page
            url = '%s/search?hl=%s&num=%d&start=%s&q=%s' % (base_url, self.lang, results_per_page, start, query)
            retry = 3
            while(retry > 0):
                try:
                    request = urllib2.Request(url)
                    user_agent = get_user_agent()
                    request.add_header('User-agent', user_agent)
                    request.add_header('connection','keep-alive')
                    request.add_header('Accept-Encoding', 'gzip')
                    request.add_header('referer', base_url)
                    response = urllib2.urlopen(request)
                    html = response.read()
                    if(response.headers.get('content-encoding', None) == 'gzip'):
                        html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()

                    self.extractSearchResults(html)
                    break;
                except urllib2.URLError,e:
                    print 'url error:', e
                    self.randomSleep()
                    retry = retry - 1
                    continue

                except Exception, e:
                    print 'error:', e
                    retry = retry - 1
                    self.randomSleep()
                    continue
        return self.search_url_list, self.search_doc_list

def main_TD(keyword='中兴', fkey='test'):
    st = SearchToutiao(keyword)
    res_list, doc_list, url_list, image_list = st.get_search_res()

    outfile = "../data/doc_" + fkey
    fwd = open(outfile, 'w')
    fwd.write(" ".join(doc_list))

    #outfile = "../data/img_" + fkey
    #fwd = open(outfile, 'w')
    #fwd.write(" ".join(image_list))
    print image_list

def main_GG(keyword='方太', fkey='test'):
    gs = Google(keyword)    
    url_list, doc_list = gs.search()

    outfile = "../data/doc_" + fkey
    if os.path.exists(outfile):
        os.remove(outfile)
    fwd = open(outfile, 'a')
    fwd.write(" ".join(doc_list))

if __name__ == "__main__":
    #main_GG()
    main_TD()

