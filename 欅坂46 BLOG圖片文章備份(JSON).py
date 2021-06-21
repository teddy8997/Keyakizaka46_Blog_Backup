#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import os
import io
import sys
import warnings
import json
from requests import exceptions
warnings.filterwarnings("ignore")

def get_html(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

def downImg(member, date, req_bs):
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    hour = date[11:13]
    minu = date[14:]
    saveDir = "./" + member +"/" +  year+ month + day + hour+ minu + "/"

    if not os.path.isdir(saveDir):
        os.makedirs(saveDir)
        
    img_list = req_bs.findAll('img')
    i = 0;
    for img in img_list:
        print(img)
        try:
            srcURL = img['src']
        except KeyError:
            print(year+ month + day + hour+ minu + "==== ERR")
            continue;
        if srcURL != '':
            try:
                tmp = requests.get(srcURL)
            except requests.exceptions.InvalidSchema :
                continue
                
            with open(saveDir + str(i) + '.jpg', 'wb') as f:
                f.write(tmp.content)
            img['src'] = year + month + day + hour + minu + '/' + str(i) + '.jpg'
        
        i += 1


member = {"上村莉菜": "03", "尾関梨香": "04", "小池美波": "06", "小林由依": "07", "齋藤冬優花": "08", "菅井友香": "11", "土生瑞穂": "14", "原田葵": "15"
          , "守屋茜": "18", "渡辺梨加": "20", "渡邉理佐": "21", "井上梨名": "43", "関有美子": "44", "武元唯衣": "45", "田村保乃": "46", "藤吉夏鈴": "47", "松田里奈": "48", "松平璃子": "49", "森田ひかる": "50", "山﨑天": "51", "遠藤光莉": "53",
         "大園玲": "54", "大沼晶保": "55", "幸阪茉里乃": "56", "増本綺良": "57", "守屋麗奈": "58"}


name = input('請輸入要下載的成員(一次輸入一個成員)：')
url = "https://www.keyakizaka46.com/s/k46o/diary/member/list?ima=0000&ct=" + str(member[name]);
req = get_html(url)
req_bs = bs(req,"html5lib")
articleList = req_bs.findAll('article')

per_ym_list = []
for article in articleList:
    timeTag = article.find(class_="box-date").findAll('time')
    date = timeTag[0].text.replace('.','') 
    title = article.find(class_="box-ttl").find('a').text
    author = article.find(class_="name").text.strip()
    contentReq = article.find(class_="box-article")
    bottomDate = article.find(class_="box-bottom").find('li').text.strip()
    downImg(author, bottomDate, contentReq)
    content = str(contentReq)
    data = {"date": bottomDate, "author": author, "title": title, "body": content, "ym": date}
    per_ym_list.append(data)

nextPage = req_bs.find(class_="pager").findAll('li')

while (nextPage[len(nextPage)-1].text == ">"):
    url = "https://www.keyakizaka46.com" + nextPage[len(nextPage)-1].find('a').get('href')
    req = get_html(url)
    req_bs = bs(req,"html5lib")
    articleList = req_bs.findAll('article')
    nextPage = req_bs.find(class_="pager").findAll('li')
    for article in articleList:
        timeTag = article.find(class_="box-date").findAll('time')
        date = timeTag[0].text.replace('.','') 
        title = article.find(class_="box-ttl").find('a').text
        author = article.find(class_="name").text.strip()
        contentReq = article.find(class_="box-article")
        bottomDate = article.find(class_="box-bottom").find('li').text.strip()
        downImg(author, bottomDate, contentReq)
        content = str(contentReq)
        
        data = {"date": bottomDate, "author": author, "title": title, "body": content, "ym": date}
        per_ym_list.append(data)
        
with open("./" + author +"/" + "result" + '.json', mode='w', encoding='utf-8') as f:
    json.dump(per_ym_list, f)
