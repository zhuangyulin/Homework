import pymongo
import requests
from lxml import etree

class Authors():
    def __init__(self):
        #创建数据库连接对象的两种方式
        self.client=pymongo.MongoClient(host='127.0.0.1')
        self.headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        }

    def run(self):
        url="https://so.gushiwen.cn/authors/"
        info=self.get_data_by_url(url)

    # 根据url去下载对应页面的HTML数据,返回页面源码字符串
    def download_data_by_url(self,url):
        try:
            response=requests.get(url,headers=self.headers)
            return response.content.decode("utf-8")
        except Exception as e:
            print(e)
            return ""

    # 根据url解析数据,返回值(data,total_page)
    def get_data_by_url(self,url):
        client=pymongo.MongoClient("mongodb://localhost:27017/")
        db=client.poetry
        col=db.authors

        content=self.download_data_by_url(url)
        content=etree.HTML(content) #构造了一个XPath解析对象并对HTML文本进行自动修正
        auth_name=content.xpath(".//div[@class='typecont']/span/a/text()")
        
        dynasty=[]
        dynasties=content.xpath("//div[@class='typecont']/span/text()")
        for dyn in dynasties:
            dyn=dyn.replace("(","").replace(")","")
            dynasty.append(dyn)
        
        auth_link=[]
        Intro=[]
        auth_links=content.xpath(".//div[@class='typecont']/span/a/@href")
        for link in auth_links:
            link="https://so.gushiwen.cn"+link
            auth_link.append(link)
        for link in auth_link:
            content=self.download_data_by_url(link)
            content=etree.HTML(content)
            Introduction=content.xpath("//div[@class='cont']/p/text()")
            
            for Intros in Introduction:
                if Intros!="\u3000":
                    Intro.append(Intros)

        auth_list={}
        for i in range(len(auth_name)):
            auth_list={
                "auth_name":auth_name[i],
                "dynasty":dynasty[i],
                "link":auth_link[i],
                "Intro":Intro[i]
            }
            col.insert(auth_list)
        print("插入成功！")
auth=Authors()  
auth.run()