#!usr/bin/env python
#-*- coding: utf-8 -*-

import os
import urllib2
import urllib
import cookielib
import xml.etree.ElementTree as ET
#-----------------------------------------------------------------------------
# Login in www.***.com.cn
def ChinaBiddingLogin(url, username, password):
    # Enable cookie support for urllib2
    cookiejar=cookielib.CookieJar()
    urlopener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    urllib2.install_opener(urlopener)
    
    urlopener.addheaders.append(('Referer', 'http://www.chinabidding.com.cn/zbw/login/login.jsp'))
    urlopener.addheaders.append(('Accept-Language', 'zh-CN'))
    urlopener.addheaders.append(('Host', 'www.chinabidding.com.cn'))
    urlopener.addheaders.append(('User-Agent', 'Mozilla/5.0 (compatible; MISE 9.0; Windows NT 6.1); Trident/5.0'))
    urlopener.addheaders.append(('Connection', 'Keep-Alive'))
    print 'XXX Login......'
    imgurl=r'http://www.*****.com.cn/zbw/login/image.jsp'
    DownloadFile(imgurl, urlopener)
    authcode=raw_input('Please enter the authcode:')
    #authcode=VerifyingCodeRecognization(r"http://192.168.0.106/images/code.jpg")
    # Send login/password to the site and get the session cookie
    values={'login_id':username, 'opl':'op_login', 'login_passwd':password, 'login_check':authcode}
    urlcontent=urlopener.open(urllib2.Request(url, urllib.urlencode(values)))
    page=urlcontent.read(500000)
    # Make sure we are logged in, check the returned page content
    if page.find('login.jsp')!=-1:
        print 'Login failed with username=%s, password=%s and authcode=%s' \
                % (username, password, authcode)
        return False
    else:
        print 'Login succeeded!'
        return True
#-----------------------------------------------------------------------------
# Download from fileUrl then save to fileToSave
# Note: the fileUrl must be a valid file
def DownloadFile(fileUrl, urlopener):
    isDownOk=False
    try:
        if fileUrl:
            outfile=open(r'/var/www/images/code.jpg', 'w')
            outfile.write(urlopener.open(urllib2.Request(fileUrl)).read())
            outfile.close()
            isDownOK=True
        else:
            print 'ERROR: fileUrl is NULL!'
    except:
        isDownOK=False
    return isDownOK
#------------------------------------------------------------------------------
# Verifying code recoginization
def VerifyingCodeRecognization(imgurl):
    url=r'http://192.168.0.119:800/api?'
    user='admin'
    pwd='admin'
    model='ocr'
    ocrfile='cbi'
    values={'user':user, 'pwd':pwd, 'model':model, 'ocrfile':ocrfile, 'imgurl':imgurl}
    data=urllib.urlencode(values)
    try:
        url+=data
        urlcontent=urllib2.urlopen(url)
    except IOError:
        print '***ERROR: invalid URL (%s)' % url
    page=urlcontent.read(500000)
    # Parse the xml data and get the verifying code
    root=ET.fromstring(page)
    node_find=root.find('AddField')
    authcode=node_find.attrib['data']
    return authcode
#------------------------------------------------------------------------------
# Read users from configure file
def ReadUsersFromFile(filename):
    users={}
    for eachLine in open(filename, 'r'):
        info=[w for w in eachLine.strip().split()]
        if len(info)==2:
            users[info[0]]=info[1]
    return users
#------------------------------------------------------------------------------
def main():
    login_page=r'http://crm.360.cn/login'
    download_page=r'http://kf.crm.360.cn/service/accountManagement/index?accountTab=search&isp=1474193752295_9983461'
    start_id=8593330
    end_id=8595000
    now_id=start_id
    Users=ReadUsersFromFile('users.conf')
    while True:
        for key in Users:
            if ChinaBiddingLogin(login_page, key, Users[key]):
                for i in range(3):
                    #pageUrl=download_page+'%d' % now_id
                    pageUrl=download_page
                    urlcontent=urllib2.urlopen(pageUrl)
                    filepath='./download/%s.html' % now_id
                    f=open(filepath, 'w')
                    f.write(urlcontent.read(500000))
                    f.close()
                    now_id+=1
            else:
                continue
#------------------------------------------------------------------------------
if __name__=='__main__':
    main()
