import pymongo
import requests
from lxml import etree

class Classical():
    def __init__(self):
        #创建数据库连接对象的两种方式
        self.client=pymongo.MongoClient(host='127.0.0.1')
        self.headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        }

    def run(self):
        urls=[]
        base_url="http://www.shifansheng.cc/daquan/rkl"
        urls.append("http://www.shifansheng.cc/daquan/rkl.html")
        # for i in range(2,14):
        #     urls.append(base_url+"_"+str(i)+".html")
        for url in urls:
            self.get_data_by_url(url)

    # 根据url去下载对应页面的HTML数据,返回页面源码字符串
    def download_data_by_url(self,url):
        try:
            response=requests.get(url,headers=self.headers)
            return response.content.decode("gb2312",errors='ignore')
        except Exception as e:
            print(e)
            return ""

    # 根据url解析数据,返回值(data,total_page)
    def get_data_by_url(self,url):
        client=pymongo.MongoClient("mongodb://localhost:27017/")
        db=client.poetry
        col=db.ClassicalChinese

        content1=self.download_data_by_url(url)
        content1=etree.HTML(content1) #构造了一个XPath解析对象并对HTML文本进行自动修正
        #一级页面
        #获取标题
        title=content1.xpath("//li/a/text()")
        #获取网址
        first_link=[]
        second_link=[]
        first_links=content1.xpath("//li/a/@href")
        for links in first_links:
            links=links.replace("..","http://www.shifansheng.cc")
            first_link.append(links)
        i=0
        info={}
        qas={}
        #进入二级页面
        for link in first_link:
            content2=self.download_data_by_url(link)
            content2=etree.HTML(content2)
            info_all=content2.xpath("//table[@id='table1']//tr[3]/td//text()")
            # info_all=content2.xpath("//td/text()")
            info[title[i]]=info_all
            i+=1
            #获取三级页面
            second_links=content2.xpath("//table[@id='table1']//a/@href")
            # print(second_links)
            if second_links==0:
                second_links='没有相关习题哇！'
                second_link.append(second_links)
            else:
                second_links=str(second_links).replace("..","http://www.shifansheng.cc")
                second_link.append(second_links)
        # print(len(first_link))        
        # print(len(second_link))
        #         j=0
        #         #进入三级页面
        #         for link2 in second_link:
        #             content3=self.download_data_by_url(link)
        #             content3=etree.HTML(content3)
        #             qa=content3.xpath("//table[@id='table1']//tr[3]/td//text()")
        # print(len(qa))
                    # qas[second_link[j]]=qa
                    # j+=1
        # 存入数据库
        for i in range(len(title)):
            infos={
                "title":title[i],
                "first_link":first_link[i],
                "info":info[title[i]],
                "second_link":second_link[i]
                # "qa":qas[second_link[j]]

            }
            col.insert(infos)
        print("插入成功！")
            

            # info_list=[]
            # info_list2=[]
            # for info_one in info_all:
            #     info_one=info_one.replace("\r\n","").replace("\r\n      ","").replace("\n\xa0\xa0\xa0\xa0","").replace("\n","").replace("\xa0\xa0\xa0\xa0","").replace("      ","").replace("    ","").replace("\xa0","")
            #     info_list.append(info_one)
            # print(info_list)
            # for j1 in info_list:
            #     print(j1) 
            #         for j2 in j1:
            #             print(j2)
            #         if len(j)!=0:
            #             info_list2.append(j)
            #             print(j)

cc=Classical()  
cc.run()