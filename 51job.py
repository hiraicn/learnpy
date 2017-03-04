#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib,re
import sys
import pymongo
reload(sys)
sys.setdefaultencoding('utf-8') #代表输出的内容是utf-8

client = pymongo.MongoClient('localhost',27017)
walden = client['51job']
sheet_tab = walden['sheet_tab']

reload(sys)
sys.setdefaultencoding('utf-8') #代表输出的内容是utf-8

def get_content(page):
    url = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=180200%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword=python&keywordtype=2&curr_page={}&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9'.format(page)
    a = urllib.urlopen(url) #打开网址
    html = a.read()
    html = html.decode('gbk')
    # print html
    return html
#中文在可迭代对象里就是unicode编码
def get(html):
    reg = re.compile(r'class="t1 ">.*?<a target="_blank" title="(.*?)".*?<span class="t2"><a target="_blank" title="(.*?)".*?<span class="t3">(.*?)</span>.*?<span class="t4">(.*?)</span>.*?<span class="t5">(.*?)</span>',re.S)
    items = re.findall(reg,html)
    # print items #列表
    return items

for j in range(1,10):
    html = get_content(j) #获取源代码
    for i in get(html):
        data = {
            '职位':i[0],
            '公司':i[1],
            '地区':i[2],
            '薪资':i[3],
            '发布日期':i[4],
        }
        sheet_tab.insert(data)
