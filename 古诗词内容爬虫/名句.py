import requests
from bs4 import BeautifulSoup
import pymongo
import re

class sentenceSpider():
    def __init__(self):
        self.base_url='https://so.gushiwen.cn/mingjus/default.aspx?page={0}&tstr={1}&astr=&cstr=&xstr='
        self.main_url = "https://so.gushiwen.cn/mingjus/default.aspx?tstr={}"
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'
        }
        # self.author_url_base="https://so.gushiwen.cn/"

    def download(self, url):
        try:
            response = requests.get(url=url, headers=self.head)
            # print('页面内容爬取完毕!')
            return response.content.decode('utf8')
        except Exception as e:
            print(e)
            return ''

    def classify(self):
        content=self.download(self.main_url)
        # print(content)
        type_url={}
        type_url_list=[]
        type_name_list=[]
        soup = BeautifulSoup(content, "lxml")
        type_all=soup.find('div',class_='main3').find('div',class_='right').find_all('div',class_='sons')
        for type_single in type_all:
            type=type_single.find('div',class_='cont').find_all('a')
            for i in type:
                type_name_list.append(i.get_text())  
                k=i.get_text()
                type_url_list.append(self.main_url.format(k))
        type_url=dict(zip(type_name_list,type_url_list))
        # print (type_url)
        return type_url

    def second_sentence(self,url,name):
        # url='https://so.gushiwen.cn/mingjus/default.aspx?tstr=%e5%86%99%e6%99%af'
        base_url_one=url
        content=self.download(base_url_one)
        soup = BeautifulSoup(content, "lxml")
        pages=soup.find('div',class_='main3').find('div',class_='left').find('div',class_='pagesright').find('span').get_text()
        page_num=re.findall("[0-9]+",pages)[0]
        pages_url=[base_url_one]
        if(int(page_num)>1):
            for i in range(2,int(page_num)+1):
                pages_url.append(self.base_url.format(i,name))
        sentence_all_list=[]
        for page_url in pages_url:
            # print(page_url)
            content1=self.download(page_url)
            soup1 = BeautifulSoup(content1, "lxml")
            sentences=soup1.find('div',class_='main3').find('div',class_='left').find('div',class_='sons').find_all('div',class_='cont')           
            for sen in sentences:

                sentence_dict={}
                
                sentence_dict['sentence']=sen.find_all('a')[0].get_text()
                if(len(sen.find_all('a'))>1):
                    sen_name_aut=sen.find_all('a')[1].get_text()
                    # sen_name=re.findall(".+《",sen_name_aut)[0].replace("《","")
                    sentence_dict['sen_name']=re.findall("《.+》",sen_name_aut)[0]
                    sentence_dict['sen_author']=sen_name_aut.split("《")[0]
                else:
                    sentence_dict['sen_name']=''
                    sentence_dict['sen_author']=''
                sentence_dict['type_classify']=name
                sentence_all_list.append(sentence_dict)
        # print(sentence_all_list)
        return sentence_all_list

    def save_data(self,all_list):
        # print(all_list)
        try:
            client = pymongo.MongoClient(host='127.0.0.1')
            db =client['poetry']
            collections = db.sentence
            for data in all_list:
                # print(data)
                collections.insert_one(data)
            print("插入成功！")
        except Exception as e:
            print(e)

    def main_sentence(self):
        type_all_url=self.classify()
        type_name=list(type_all_url.keys())
        type_urls=list(type_all_url.values())
        dict1={}
        for i in range(len(type_urls)):
            every_list=self.second_sentence(type_urls[i],type_name[i])
            self.save_data(every_list)
        print('存储完成')

if __name__ == "__main__":
    
    sentence=sentenceSpider()
    sentence.main_sentence()
