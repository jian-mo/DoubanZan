# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 09:01:06 2012

@author: 毕达哥斯拉
"""
from douban_client import DoubanClient
import mechanize
import cookielib
import datetime
import re
from datetime import datetime

import time                                    #读取当前时间
now=datetime.time(datetime.now())
hour=now.hour


def autopraise(id0):
    

    #需要申请一个豆瓣API KEY， 在这里申请 http://developers.douban.com/apikey/apply
    API_KEY = ''
    API_SECRET = ''

    # 在 OAuth 2.0 中，
    # 获取权限需要指定相应的 scope，请注意!!
    SCOPE = 'shuo_basic_r,shuo_basic_w,miniblog_basic_r,miniblog_basic_w'
    callback="http://www.XXXX.com/callback"                #填你申请时候的回调地址，有没有网站都无所谓
    client = DoubanClient(API_KEY, API_SECRET, callback, SCOPE)

    # 存储授权地址
    authurl=client.authorize_url
    # print authurl
    f=open("c:/authurl.txt","w")


    # # 读取页面源代码
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

    #模拟浏览器行为
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/4.0.0')]
    r2=br.open(authurl)

    br.select_form(nr=1)
    br['user_email']=''                #你的豆瓣用户名和密码
    br['user_passwd']=''               
    r3=br.submit()

 
    c=r3.geturl()
    f.write(c)    


    #从请求页面回调地址中查找code
    m=re.findall("(?<=code\=).*",c)
    code=m[0]
    print code


    # 用code授权client
    client.auth_with_code(code)

    #获取最近广播数据

    r4=br.open("http://api.douban.com/shuo/v2/statuses/home_timeline?count=5")   #Count这里可以修改获取的广播数量，5比较多
    caststr=r4.read()
    id1=re.findall("(?<=id\"\:)\d+",caststr)
    
    
    #友邻白名单
    def whitelist():
        r1=br.open("http://api.douban.com/shuo/v2/statuses/user_timeline/XXXX")  #XXXX处 填写你不想赞的友邻用户名
        cast1=r1.read()
        id1=re.findall("(?<=id\"\:)\d+",cast1)
        id=id1
        
        return id
    
    
    f.write(caststr)                        #存储广播列表
    


    for id in id1:
        if id in id0:
            break 
        if id in whitelist():
            break      

        client.miniblog.like(id)  #赞
        print "liked"
        if hour>2 and hour<7:
            client.miniblog.comment.new(id,"Yo，watch body young man")           #提醒友邻睡觉啦
            pass


    return id1
        
    
id0=[]   
while True:                         #开赞
    id0=autopraise(id0)
    time.sleep(10)
    print "Take a Nap"
    print "id0 is ",id0