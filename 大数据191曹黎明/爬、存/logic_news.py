from selenium import webdriver
from selenium.webdriver import ActionChains
import csv
import codecs
import requests
import re
import json
import time
import random
import pymysql
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lxml import etree

driver = webdriver.Chrome('../../chromedriver')
f = open('../data/logic_news.csv', 'w', encoding='utf-8-sig')
writer = csv.writer(f)
print("Loading...................................")
driver.get('https://news.cctv.com/tech/?spm=C94212.P4YnMod9m2uD.0.0')
time.sleep(1)
newsNodes = driver.find_elements_by_css_selector('.con ul li')
news_list = []
count = 63
for newsNode in newsNodes:
    news_dict = {}
    count += 1
    news_dict["id"] = count
    title = newsNode.find_element_by_css_selector('.text_con .title a').text
    news_dict["title"] = title
    url = newsNode.find_element_by_css_selector('.text_con .title a').get_attribute('href')
    news_dict["url"] = url
    img_src = newsNode.find_element_by_css_selector('.image a img').get_attribute('data-echo')
    news_dict['img_src'] = img_src
    brief = newsNode.find_element_by_css_selector('.text_con .brief a').text
    news_dict['brief'] = brief
    news_list.append(news_dict)
driver.quit()

for news in news_list:
    http = news['url']
    response = requests.get(http, headers={
        'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'})
    content = response.content.decode("utf-8")
    content = etree.HTML(content)
    message = content.xpath("//*[@id=\"content_area\"]/p/text()")
    message = "".join(message)
    message = message.replace(" ", "").replace("\r\n", "").replace("\t", "").replace("　　", "")
    news['message'] = message
writer.writerow(['id', 'title', 'brief', 'url', 'img_src', 'message'])
for final in news_list:
    writer.writerow([final['id'], final['title'], final['brief'], final['url'], final['img_src'], final['message']])

f.close()
print("存贮结束")
