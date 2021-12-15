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
f = open('../data/fight_news.csv', 'w', encoding='utf-8-sig')
writer = csv.writer(f)
print("Loading...................................")
driver.get('https://military.cctv.com/?spm=C94212.PZd4MuV7QTb5.0.0')
time.sleep(1)
driver.find_element_by_css_selector('#open_box a').click()
time.sleep(2)
newsNodes = driver.find_elements_by_css_selector('#leftContent .ecoA9805_con02')
news_list = []
count = 123
for newsNode in newsNodes:
    news_dict = {}
    count += 1
    news_dict["id"] = count
    title = newsNode.find_element_by_css_selector('h3 span a').text
    news_dict["title"] = title
    url = newsNode.find_element_by_css_selector('h3 span a').get_attribute('href')
    news_dict["url"] = url
    img_src = newsNode.find_element_by_css_selector('.text_box .l a img').get_attribute('src')
    news_dict['img_src'] = img_src
    brief = newsNode.find_element_by_css_selector('p').text
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
