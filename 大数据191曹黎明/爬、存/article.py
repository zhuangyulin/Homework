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

driver = webdriver.Chrome('../chromedriver')
f = open('article_t.csv', 'w', encoding='utf-8-sig')
writer = csv.writer(f)
story_list = []
print("Loading...................................")
driver.get('https://www.9gexing.com/hongse/')
time.sleep(1)

for i in range(16):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
storyLists = driver.find_elements_by_css_selector('.lbox li')
for storyList in storyLists:
    story_dict = {}
    title = storyList.find_element_by_css_selector('.blogtitle a').text
    story_dict['title'] = title
    brief = storyList.find_element_by_css_selector('.blogtext').text
    story_dict['brief'] = brief
    url = storyList.find_element_by_css_selector('a').get_attribute("href")
    story_dict['url'] = url
    story_list.append(story_dict)
driver.quit()

for story in story_list:
    http = story['url']
    response = requests.get(http, headers={
        'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'})
    content = response.content.decode("utf-8")
    content = etree.HTML(content)
    message = content.xpath("//div[1]/div[1]/div/p/text()")
    message = "".join(message)
    message = message.replace(" ", "").replace("\r\n", "").replace("\t", "").replace(
        "\xa0本站信息均来自网络，如果侵犯了您的权利，请及时联系我们，我们将会及时处理。上一篇：下一篇：", "")
    story['message'] = message
for final in story_list:
    writer.writerow([final['title'], final['brief'], final['url'], final['message']])
f.close()
# print(story_list)
print("存贮结束")
