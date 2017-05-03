#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re
import pymongo


client = pymongo.MongoClient('localhost',27017)
dbName = 'qcwy'
dbTable ='job'
tab = client[dbName][dbTable]

def get_content(page):
    url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,python,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=14&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(page)
    a = requests.get(url) #打开网址
    a.encoding = 'gbk'
    html = a.text
    return html

def get(html):
    reg = re.compile(r'class="t1 ">.*?<a target="_blank" title="(.*?)".*?href="(.*?)".*?<span class="t2"><a target="_blank" title="(.*?)".*?<span class="t3">(.*?)</span>.*?<span class="t4">(.*?)</span>.*?<span class="t5">(.*?)</span>',re.S)
    items = re.findall(reg,html)
    return items
get(get_content(1))
for j in range(1,20): #选择爬取页数范围
    html = get_content(j) #获取源码
    for i in get(html):
        data = {
            '职位':i[0],
            '网站链接':i[1],
            '公司':i[2],
            '地区':i[3],
            '薪资':i[4],
            '发布日期':i[5],
        }
        tab.insert(data)

