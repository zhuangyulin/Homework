import re
import json
import time
import random
from lxml import etree
# import pymysql
import requests
from lxml import etree
import requests
from pymongo import MongoClient
import gridfs
import os
poem=[]
poem_name=[]
poem_author=[]
author_year=[] 
poem=[]
poem_name=[]
poem_author=[]
author_year=[]
class Gushici():

    def __init__(self):
        self.base_url = "https://so.gushiwen.cn/shiwens/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        }

    def url_list(self):
        urls=[]
        sec_urls=[]
        shi=[]
        ci=[]
        qu=[]
        wen=[]
        r = requests.get(self.base_url, headers=self.headers)
        r.encoding = "UTF-8"
        content = etree.HTML(r.content)

        type=content.xpath('//*[@id="html"]/body/div[2]/div[1]/div[1]/div[5]/div[2]//@href')
        for i in type:
            i=list(i)
            i.insert(22, 'page= &')
            i.insert(0, 'https://so.gushiwen.cn')
            i="".join(i)
            urls.append(i)
        for i in urls:
            for page in range(1,11):
                page=str(page)
                url_second=i.replace(' ',page)
                r = requests.get(url_second, headers=self.headers)
                r.encoding = "UTF-8"
                content = etree.HTML(r.content)
                sec_url=content.xpath('//*[@class="sons"]/div[1]/p[1]//@href')
                # sec_urls.append(page)
                sec_urls.append(sec_url)
        

        a=0
        for i in sec_urls:
            a=a+1
            i=str(i)
            i=i.replace("'","")
            i=i.split(",")
            for j in range(len(i)):
            # print(i[0])
                i[j]=i[j].replace("[","").replace("]","").replace(" ","")
                i[j]='https://so.gushiwen.cn'+i[j]
                if(a>=1 and a<=10):
                    shi.append(i[j])
                
                elif(a>=11 and a<=20):
                    ci.append(i[j])
                    
                elif(a>=21 and a<=30):
                    qu.append(i[j])
                    
                else:
                    wen.append(i[j])
           
        return shi,ci,qu,wen


    def get_main_inf(self,list1):
        for i in list1:
            r = requests.get(i, headers=self.headers)
            r.encoding = "UTF-8"
            content = etree.HTML(r.content)
            poem_0=(i[31:43])
            p_name = content.xpath("//div[@class='sons']//div//h1//text()")
            p_author = content.xpath("//div[@id='sonsyuanwen']//div//p//a[1]//text()")
            poem_1=content.xpath("//*[@id='contson"+poem_0+"']//text()")
            a_year=content.xpath("//div[@id='sonsyuanwen']//div//p//a[2]//text()")
            if p_author=='':
                p_author='佚名'
                a_year='未知'
            poem.append(poem_1)
            # print(poem_1)
            # break
            poem_name.append(p_name)
            poem_author.append(p_author)
            author_year.append(a_year)
                
                            
        for i in range(len(poem)):
            poem[i]=str(poem[i])
            poem[i]=poem[i].replace("\\n","").replace("', '","").replace("'","").replace("[","").replace("]","").replace("\u3000","")
            # print(poem)
        for i in range(len(author_year)):
            author_year[i]=str(author_year[i])
            author_year[i]=author_year[i].replace("'〔","").replace("〕'","").replace("[","").replace("]","").replace("\u3000","")
            # print(author_year[i])
        for i in range(len(poem_author)):
            poem_author[i]=str(poem_author[i])
            poem_author[i]=poem_author[i].replace("'","").replace("[","").replace("]","").replace("\u3000","") 
            # print(poem_author[i])
        for i in range(len(poem_name)):
            poem_name[i]=str(poem_name[i])
            poem_name[i]=poem_name[i].replace("[","").replace("]","").replace("'","").replace("\u3000","")

        # print(shi)
        # print(ci)
        # print(qu)
        # print(wen)
test=Gushici()
shi,ci,qu,wen=test.url_list()
test.get_main_inf(wen)
list1=['作者名','作者朝代','文言文名','内容']
poem_list=[]
for i in range(len(poem)):
          list_poem=[]
          list_poem.clear()
          list_poem.append(poem_author[i])
          list_poem.append(author_year[i])
          list_poem.append(poem_name[i])
          list_poem.append(poem[i])
          # print(list_poem)
          d=zip(list1,list_poem)
          # print(dict(d))
          # print(type(d))
          poem_list.append(dict(d))
# print(poem_list)

import pymongo
from pymongo import MongoClient
import gridfs
import os
client=MongoClient('localhost',27017)

def save_data():
        gushi=Gushici()
        gushi.url_list()
        print(poem_list)
        try:
            client = pymongo.MongoClient(host='127.0.0.1')
            db =client['poetry']
            collections = db.wenyanxhuy
            for data in poem_list:
          #       print(data)
                collections.insert_one(data)
            print("插入成功！")
        except Exception as e:
            print(e)

save_data()