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
        print(content)
        auth_name=content.xpath(".//div[@class='typecont']/span/a/text()")
        #朝代
        dynasty=[]
        dynasties=content.xpath("//div[@class='typecont']/span/text()")
        for dyn in dynasties:
            dyn=dyn.replace("(","").replace(")","")
            dynasty.append(dyn)

        #二级页面网址
        auth_link=[]
        Intro=[]
        pic=[]
        auth_links=content.xpath(".//div[@class='typecont']/span/a/@href")
        for link in auth_links:
            link="https://so.gushiwen.cn"+link
            auth_link.append(link)
        #分别进入二级页面进行操作
        for link in auth_link:
            content2=self.download_data_by_url(link)
            content2=etree.HTML(content2)
            #二级页面的作者详情
            Introduction=content2.xpath("//div[@class='cont']/p/text()")
            # print(len(Introduction))
            #清洗详情数据
            for Intros in Introduction: #不用循环会使得插入到数据库中的是数组
                if Intros!="\u3000":
                    Intro.append(Intros)
            
            #作者照片
            picture=content2.xpath("//div[@class='divimg']/img/@src")
            if len(picture)==0:
                picture='没有他的照片呀！'
                pic.append(picture)
            else:
                pic.append(picture)
        # print(pic)
        

        # # 存入数据库
        # auth_list={}
        # for i in range(len(auth_name)):
        #     auth_list={
        #         # "auth_name":auth_name[i],
        #         # "dynasty":dynasty[i],
        #         # "link":auth_link[i],
        #         # "Intro":Intro[i],
        #         # "Picture":pic[i][0] #pic是个二维数组
        #     }
        #     col.insert(auth_list)
        # print("插入成功！")
auth=Authors()  
auth.run()