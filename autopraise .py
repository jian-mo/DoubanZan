# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 09:01:06 2012

@author: �ϴ��˹��
"""
from douban_client import DoubanClient
import mechanize
import cookielib
import datetime
import re
from datetime import datetime

import time                                    #��ȡ��ǰʱ��
now=datetime.time(datetime.now())
hour=now.hour


def autopraise(id0):
    

    #��Ҫ����һ������API KEY�� ���������� http://developers.douban.com/apikey/apply
    API_KEY = ''
    API_SECRET = ''

    # �� OAuth 2.0 �У�
    # ��ȡȨ����Ҫָ����Ӧ�� scope����ע��!!
    SCOPE = 'shuo_basic_r,shuo_basic_w,miniblog_basic_r,miniblog_basic_w'
    callback="http://www.XXXX.com/callback"                #��������ʱ��Ļص���ַ����û����վ������ν
    client = DoubanClient(API_KEY, API_SECRET, callback, SCOPE)

    # �洢��Ȩ��ַ
    authurl=client.authorize_url
    # print authurl
    f=open("c:/authurl.txt","w")


    # # ��ȡҳ��Դ����
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    #ģ���������Ϊ
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/4.0.0')]
    r2=br.open(authurl)

    br.select_form(nr=1)
    br['user_email']=''                #��Ķ����û���������
    br['user_passwd']=''               
    r3=br.submit()

 
    c=r3.geturl()
    f.write(c)    


    #������ҳ��ص���ַ�в���code
    m=re.findall("(?<=code\=).*",c)
    code=m[0]
    print code


    # ��code��Ȩclient
    client.auth_with_code(code)

    #��ȡ����㲥����

    r4=br.open("http://api.douban.com/shuo/v2/statuses/home_timeline?count=5")   #Count��������޸Ļ�ȡ�Ĺ㲥������5�Ƚ϶�
    caststr=r4.read()
    id1=re.findall("(?<=id\"\:)\d+",caststr)
    
    
    #���ڰ�����
    def whitelist():
        r1=br.open("http://api.douban.com/shuo/v2/statuses/user_timeline/XXXX")  #XXXX�� ��д�㲻���޵������û���
        cast1=r1.read()
        id1=re.findall("(?<=id\"\:)\d+",cast1)
        id=id1
        
        return id
    
    
    f.write(caststr)                        #�洢�㲥�б�
    


    for id in id1:
        if id in id0:
            break 
        if id in whitelist():
            break      

        client.miniblog.like(id)  #��
        print "liked"
        if hour>2 and hour<7:
            client.miniblog.comment.new(id,"Yo��watch body young man")           #��������˯����
            pass


    return id1
        
    
id0=[]   
while True:                         #����
    id0=autopraise(id0)
    time.sleep(10)
    print "Take a Nap"
    print "id0 is ",id0