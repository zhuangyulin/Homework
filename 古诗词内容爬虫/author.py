
import requests
from bs4 import BeautifulSoup
import pymongo
import re

class authorSpider():
    def __init__(self):
        self.base_url = "https://so.gushiwen.cn/authors/Default.aspx?p=1&c={0}"
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'
        }
        self.author_url_base="https://so.gushiwen.cn/"

    def download(self, url):
        try:
            response = requests.get(url=url, headers=self.head)
            # print('页面内容爬取完毕!')
            return response.content.decode('utf8')
        except Exception as e:
            print(e)
            return ''
    
    def get_second_data(self,url):
        second_list=[]
        # url='https://so.gushiwen.cn/authorv_f59c39d8cecd.aspx'
        content=self.download(url)
        # print(content)
        soup = BeautifulSoup(content, "lxml")
        introductions=soup.find('div',class_='main3').find('p').stripped_strings
        introductions=list(introductions)
        introduction=introductions[0]
        if(len(introductions))>=3:
            poems_num=re.findall("[0-9].+",introductions[1])[0]
            sentence_num=re.findall("[0-9].+",introductions[2])[0]
        elif(len(introductions))==2:
            
            if(len(re.findall("诗文",introductions[1]))!=0):
                poems_num=re.findall("[0-9].+",introductions[1])[0]
                sentence_num=''
            else:
                poems_num=''
                sentence_num=re.findall("[0-9].+",introductions[1])[0]
        else:
            poems_num=''
            sentence_num=''
        second_list.append(introduction)
        second_list.append(poems_num)
        second_list.append(sentence_num)
        return(second_list) 

    def get_main_data(self):
        all_url=[]
        dynastys=['先秦','两汉','魏晋','南北朝','隋代','唐代','五代','宋代','金朝','元代','明代','清代']
        for i in dynastys:
            url=self.base_url.format(i)
            all_url.append(url)
            print(url)
        all_list=[]
        i=0
        for url in all_url:
            content1=self.download(url)
            # print(content1)
            soup = BeautifulSoup(content1, "lxml")
            author_list=soup.find("div",class_='typecont').find_all("span")
            # print(author_list)
            for span in author_list:
                author_dict={}
                author=span.get_text()
                herf=span.find("a").get('href')
                author_dict['author']=author
                author_dict['dynasty']=dynastys[i]
                herf=self.author_url_base+herf
                # all_herf.append(self.author_url_base+herf)
                introduction=self.get_second_data(herf)[0]
                author_dict['introduction']=introduction
                poems_num=self.get_second_data(herf)[1]
                sentence_num=self.get_second_data(herf)[2]
                author_dict['poems_num']=poems_num
                author_dict['sentence_num']=sentence_num
                all_list.append(author_dict)
                # print(all_list)
            print('{} 作者已爬完'.format(dynastys[i]))
            i=i+1
        return all_list


    def save_data(self):
        all_list=self.get_main_data()
        # print(all_list)
        try:
            client = pymongo.MongoClient(host='127.0.0.1')
            db =client['poetry']
            collections = db.author1
            for data in all_list:
                # print(data)
                collections.insert_one(data)
            print("插入成功！")
        except Exception as e:
            print(e)
if __name__ == "__main__":
    
    auth=authorSpider()
    auth.save_data()
    # auth.get_second_data()
    # auth.get_main_data()


       


        