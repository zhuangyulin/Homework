from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import pymongo

def spider(url):
    #设置User-Agent
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}    
    req_timeout = 5
    req = Request(url=url, headers=headers)
    #urlopen实现对url的访问，第一个参数可以是url也可是一个request，data=None
    f = urlopen(req, None, req_timeout)
    s = f.read()
    s = s.decode("utf-8")
    #用beautifulsoup爬取网页内容,第一个参数是指定解析的内容，第二个参数是指定解析器为html.parser
    bs = BeautifulSoup(s, 'html.parser')
    #find_all找出所有auther的链接
    soup = bs.find(class_='sons',id='right1')
    soups = soup.find(class_='cont')
    links = soups.find_all('a')
    list={}
    href=[]
    name_list=[]
    for link in links:
        # print(link.string)
        # print(link['href'])
        name=link.string
        href=link['href']
        # print(type(href))
        # print(type(name))
        # return name,href
        name_list=name.split(" ")
        href_link=href.split(" ")
        for i in range(len(name_list)):
            list={
                "auth_name":name_list[i],
                "href":href_link[i],
            }
            col.insert(list)
        print("插入成功！")

# print(datas)
# print(name,href)
        
try:
    #导入并定义mongodb数据库
    client = pymongo.MongoClient('localhost', 27017)
    auther = client['auther']  # 创建数据库
    inf = auther['inf']  # 创建表
    col=auther.inf
    data=spider('https://so.gushiwen.cn/authors/')
except Exception as e:
    print(e)
