import requests
import re
import json
from lxml import etree
from pymongo import MongoClient
import gridfs
import os
client=MongoClient('localhost',27017)
connect = MongoClient('127.0.0.1', 27017)  # 创建连接点
test = connect.test
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
        self.base_url = "https://so.gushiwen.cn/gushi/tangshi.aspx"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }

    def url_list(self):
        urls=[]
        r = requests.get(self.base_url, headers=self.headers)
        r.encoding = "UTF-8"
        content = etree.HTML(r.content)

        type=content.xpath('//*[@id="html"]/body/div[2]/div[2]/div[1]/div[2]//@href')

        for types in type:
            if types[0]=='/':
                types='https://so.gushiwen.cn'+types
                # print(types)
            r = requests.get(types, headers=self.headers)
            r.encoding = "UTF-8"
            content = etree.HTML(r.content)
            url = content.xpath("//div[@class='sons']//div//span//@href")
            for i in range(len(url)):
                if url[i][0]=='/':
                    url[i]='https://so.gushiwen.cn'+url[i]
                urls.append(url[i])
        l2 = list(set(urls))
        l2.sort(key=urls.index)
        # print(len(l2))
        # print(l2)
        return l2


    def url_second(self):
            url=self.url_list()
            a=0
            for i in url:
                if a<=7800:
                    r = requests.get(i, headers=self.headers)
                    r.encoding = "UTF-8"    
                    content = etree.HTML(r.content)
                    poem_0=(i[31:43])
                        # print(poem_0)
                        # break
                    p_name = content.xpath("//div[@class='sons']//div//h1//text()")
                    p_author = content.xpath("//div[@id='sonsyuanwen']//div//p//a[1]//text()")
                    poem_1=content.xpath("//*[@id='contson"+poem_0+"']//text()")
                    a_year=content.xpath("//div[@id='sonsyuanwen']//div//p//a[2]//text()")
                        # print(poem_1)
                        # break
                        # print(a_year)
                        # break
                    if p_author=='':
                        p_author='佚名'
                        a_year='未知'
                    poem.append(poem_1)
                    print(poem_1)
                    # break
                    poem_name.append(p_name)
                    poem_author.append(p_author)
                    author_year.append(a_year)
                    a=a+1
                
                
                            
            for i in range(len(poem)):
                poem[i]=str(poem[i])
#               print(i)
                poem[i]=poem[i].replace("\\n","").replace("', '","").replace("'","").replace("[","").replace("]","").replace("\u3000","")
            for i in range(len(author_year)):
                author_year[i]=str(author_year[i])
                author_year[i]=author_year[i].replace("'〔","").replace("〕'","").replace("[","").replace("]","").replace("\u3000","")
                print(author_year[i])
            for i in range(len(poem_author)):
                poem_author[i]=str(poem_author[i])
                poem_author[i]=poem_author[i].replace("'","").replace("[","").replace("]","").replace("\u3000","") 
                print(poem_author[i])
            for i in range(len(poem_name)):
                poem_name[i]=str(poem_name[i])
                poem_name[i]=poem_name[i].replace("[","").replace("]","").replace("'","").replace("\u3000","") 
            #   print(poem)
            # print(i)
            # print(poem_name)
            # print(poem_author)
            # print(author_year)


# list1 = ['1','2','3']
# list2 = ['a','b','c']
# list3 = ['A','B','C']
# d={}
# d=zip(list1,(list2, list3))
# print(d)
list1=['作者名','诗词名','诗词','作者朝代']
poem_list=[]
for i in range(len(poem)):
          list_poem=[]
          list_poem.clear()
          list_poem.append(poem_author[i])
          list_poem.append(poem_name[i])
          list_poem.append(poem[i])
          list_poem.append(author_year[i])
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
        print(poem_list)
        try:
            client = pymongo.MongoClient(host='127.0.0.1')
            db =client['poetry']
            collections = db.poem
            for data in poem_list:
          #       print(data)
                collections.insert_one(data)
            print("插入成功！")
        except Exception as e:
            print(e)

save_data()