import random
import re
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver

tablename = 'main_data'  # 数据表名
host = 'localhost'  # 数据库地址
user = 'root'  # 数据库用户名
password = '1234'  # 数据库密码
dbase = 'voachinese'  # 数据库名
chromedriver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver"


def createtable():  # 建数据表
    db = pymysql.connect(host=host, user=user, password=password, db=dbase)
    cursor = db.cursor()
    # tablename = tablename_base + '_test01'
    sql = '''
       CREATE TABLE `{}`(
               `title` varchar(255) NOT NULL,
               `url` varchar(255) default NULL,
               `brief` varchar(255) default NULL,
               `detail` text(65500) default NULL,
               `label` varchar(255) DEFAULT NULL,
               PRIMARY KEY  (`title`)
               )ENGINE=InnoDB DEFAULT CHARSET=utf8;
       '''.format(tablename)
    try:
        cursor.execute(sql)
        db.commit()
        print('新建数据表成功！')
    except Exception as e:
        db.rollback()
        print('新建数据表失败！{}'.format(e))
    finally:
        cursor.close()
        db.close()


#################################################################################################################
class Fight_news:
    def __init__(self, count, url):
        self.base_url = url
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.count = count

    def get_brief_message(self):
        news_list = []
        driver = webdriver.Chrome(chromedriver)
        print("Loading...................................")
        driver.get(self.base_url)
        driver.find_element_by_css_selector('#open_box a').click()
        newsNodes = driver.find_elements_by_css_selector('#leftContent .ecoA9805_con02')
        for newsNode in newsNodes:
            news_dict = {}
            self.count += 1
            news_dict["id"] = self.count
            title = newsNode.find_element_by_css_selector('h3 span a').text
            news_dict["title"] = title
            url = newsNode.find_element_by_css_selector('h3 span a').get_attribute('href')
            news_dict["url"] = url
            img_src = newsNode.find_element_by_css_selector('.text_box .l a img').get_attribute('src')
            news_dict['img_src'] = img_src
            brief = newsNode.find_element_by_css_selector('p').text
            news_dict['brief'] = brief
            news_list.append(news_dict)
            print("文章{}获取完成".format(title))
        print('********数据获取完毕********')
        driver.quit()
        return news_list

    def get_detail(self, news_list):
        for news in news_list:
            http = news['url']
            response = requests.get(http, headers=self.head)
            content = response.content.decode("utf-8")
            print("{}下载完成".format(news['url']))
            content = etree.HTML(content)
            message = content.xpath("//*[@id=\"content_area\"]/p/text()")
            message = "".join(message)
            message = message.replace(" ", "").replace("\r\n", "").replace("\t", "").replace("　　", "")
            news['message'] = message
        # writer.writerow(['id', 'title', 'brief', 'url', 'img_src', 'message'])
        # for final in news_list:
        # print(final)
        return news_list

    def write_date(self, list_dic):  # 存数据
        db = pymysql.connect(host=host, user=user, password=password, db=dbase)
        cursor = db.cursor()
        # tablename = tablename_base + '_test01'
        sql_table = '''   
                show tables
                '''
        cursor.execute(sql_table)  # 数据表查重
        tables = cursor.fetchall()
        tables_list = re.findall('(\'.*?\')', str(tables))
        tables_list = [re.sub("'", '', each) for each in tables_list]
        if tablename in tables_list:
            # print("数据表已存在！")
            pass
        else:
            createtable()
        # print("write_date:")
        # print(list_dic['title'], list_dic['url'], list_dic['brief'], list_dic['detail'])
        sql = '''
        insert into {}(title,url,brief,detail) values('{}','{}','{}','{}')
        '''.format(tablename, list_dic['title'], list_dic['url'], list_dic['brief'], list_dic['message'])
        try:
            cursor.execute(sql)  # 写入数据
            db.commit()
            print("{} 写入数据成功！".format(list_dic['title']))
        except Exception as e:
            print("写入数据失败！{}".format(e))
            db.rollback()
        finally:
            cursor.close()
            db.close()

    def run(self):
        news_list = self.get_detail(self.get_brief_message())
        for news_dic in news_list:
            self.write_date(news_dic)


###################################################################################################################
class Logic_news:
    def __init__(self, count, url):
        self.base_url = url
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.count = count

    def get_brief_message(self):  # 获取所有文章标题、简介、二级页面网址
        news_list = []
        driver = webdriver.Chrome(chromedriver)
        print("Loading...................................")
        driver.get(self.base_url)
        time.sleep(1)
        newsNodes = driver.find_elements_by_css_selector('.con ul li')
        # count = 63
        for newsNode in newsNodes:
            news_dict = {}
            self.count += 1
            news_dict["id"] = self.count
            title = newsNode.find_element_by_css_selector('.text_con .title a').text
            news_dict["title"] = title
            url = newsNode.find_element_by_css_selector('.text_con .title a').get_attribute('href')
            news_dict["url"] = url
            img_src = newsNode.find_element_by_css_selector('.image a img').get_attribute('data-echo')
            news_dict['img_src'] = img_src
            brief = newsNode.find_element_by_css_selector('.text_con .brief a').text
            news_dict['brief'] = brief
            news_list.append(news_dict)
            print("文章{}获取完成".format(title))
        print('********数据获取完毕********')
        # print(news_dict)
        driver.quit()
        return news_list

    def get_detail(self, news_list):
        for news in news_list:
            http = news['url']
            response = requests.get(http, headers=self.head)
            content = response.content.decode("utf-8")
            print("{}下载完成".format(news['url']))
            content = etree.HTML(content)
            message = content.xpath("//*[@id=\"content_area\"]/p/text()")
            message = "".join(message)
            message = message.replace(" ", "").replace("\r\n", "").replace("\t", "").replace("　　", "")
            news['message'] = message
        # writer.writerow(['id', 'title', 'brief', 'url', 'img_src', 'message'])
        # for final in news_list:
        # print(final)
        return news_list

    def write_date(self, list_dic):  # 存数据
        db = pymysql.connect(host=host, user=user, password=password, db=dbase)
        cursor = db.cursor()
        # tablename = tablename_base + '_test01'
        sql_table = '''   
                show tables
                '''
        cursor.execute(sql_table)  # 数据表查重
        tables = cursor.fetchall()
        tables_list = re.findall('(\'.*?\')', str(tables))
        tables_list = [re.sub("'", '', each) for each in tables_list]
        if tablename in tables_list:
            # print("数据表已存在！")
            pass
        else:
            createtable()
        # print("write_date:")
        # print(list_dic['title'], list_dic['url'], list_dic['brief'], list_dic['detail'])
        sql = '''
        insert into {}(title,url,brief,detail) values('{}','{}','{}','{}')
        '''.format(tablename, list_dic['title'], list_dic['url'], list_dic['brief'], list_dic['message'])
        try:
            cursor.execute(sql)  # 写入数据
            db.commit()
            print("{} 写入数据成功！".format(list_dic['title']))
        except Exception as e:
            print("写入数据失败！{}".format(e))
            db.rollback()
        finally:
            cursor.close()
            db.close()

    def run(self):
        news_list = self.get_detail(self.get_brief_message())
        for news_dic in news_list:
            self.write_date(news_dic)


######################################################################################################################
class HotStory:
    def __init__(self):
        self.base_url = 'https://www.9gexing.com/hongse/'
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # tablename_base = 'hotstory'

    def download_second_page(self, url):  # 下载正文内容
        try:
            times = [0.3, 0.8, 1.1, 0.5, 1.4]
            time.sleep(random.choice(times))
            response = requests.get(url, headers=self.head)
            print('{} 页面内容下载完成！'.format(url))
            return response.content.decode('utf8')
        except Exception as e:
            print('{} 页面内容下载失败！{}'.format(url, e))
            return ''

    def get_detail_messgae(self, content):  # 正文内容清洗
        content = etree.HTML(content)
        message = content.xpath("//div[1]/div[1]/div/p/text()")
        message = "".join(message)
        message = message.replace(" ", "").replace("\r\n", "").replace("\t", "").replace(
            "\xa0本站信息均来自网络，如果侵犯了您的权利，请及时联系我们，我们将会及时处理。上一篇：下一篇：", "")
        print("页面分析完毕!")
        return message
        # story['message'] = message

    def get_brief_message(self):  # 获取所有文章标题、简介、二级页面网址
        story_list = []
        driver = webdriver.Chrome(chromedriver)
        print("Loading...................................")
        driver.get('https://www.9gexing.com/hongse/')
        for i in range(4):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(random.uniform(0.2, 1))
        storyLists = driver.find_elements_by_css_selector('.lbox li')
        for storyList in storyLists:
            story_dict = {}
            title = storyList.find_element_by_css_selector('.blogtitle a').text
            story_dict['title'] = title
            brief = storyList.find_element_by_css_selector('.blogtext').text
            story_dict['brief'] = brief
            url = storyList.find_element_by_css_selector('a').get_attribute("href")
            story_dict['url'] = url
            detail = self.get_detail_messgae(self.download_second_page(url))
            story_dict['detail'] = detail
            # print(story_dict)
            story_list.append(story_dict)
        driver.quit()
        print("********数据获取完毕********")
        return story_list

    def write_date(self, list_dic):  # 存数据
        db = pymysql.connect(host=host, user=user, password=password, db=dbase)
        cursor = db.cursor()
        # tablename = tablename_base + '_test01'
        sql_table = '''   
                show tables
                '''
        cursor.execute(sql_table)  # 数据表查重
        tables = cursor.fetchall()
        tables_list = re.findall('(\'.*?\')', str(tables))
        tables_list = [re.sub("'", '', each) for each in tables_list]
        if tablename in tables_list:
            # print("数据表已存在！")
            pass
        else:
            createtable()
        # print("write_date:")
        # print(list_dic['title'], list_dic['url'], list_dic['brief'], list_dic['detail'])
        sql = '''
        insert into {}(title,url,brief,detail) values('{}','{}','{}','{}')
        '''.format(tablename, list_dic['title'], list_dic['url'], list_dic['brief'], list_dic['detail'])
        try:
            cursor.execute(sql)  # 写入数据
            db.commit()
            print("{} 写入数据成功！".format(list_dic['title']))
        except Exception as e:
            print("写入数据失败！{}".format(e))
            db.rollback()
        finally:
            cursor.close()
            db.close()

    def run(self):
        storys = self.get_brief_message()
        # print("run story_list:{}".format(storys))
        for list_dic in storys:
            # print("run list_dic: {}".format(list_dic))
            self.write_date(list_dic)


if __name__ == "__main__":
    hotstory = HotStory()
    hotstory.run()
    logic = Logic_news(63, 'https://news.cctv.com/tech/?spm=C94212.P4YnMod9m2uD.0.0')
    logic.run()
    internation = Logic_news(83, 'https://news.cctv.com/world/?spm=C94212.PGZDd8bkBJCZ.0.0')
    internation.run()
    law = Logic_news(103, 'https://news.cctv.com/law/?spm=C94212.PGZDd8bkBJCZ.0.0')
    law.run()
    fight = Fight_news(123, 'https://military.cctv.com/?spm=C94212.PZd4MuV7QTb5.0.0')
    fight.run()
