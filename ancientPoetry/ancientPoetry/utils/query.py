#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: xxx  time: 2021/6/29
import os

import pandas as pd
import numpy as np
import jieba
import re
import codecs
import pymongo
# from textblob import TextBlob

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # refers to application_top
APP_STATIC_TXT = os.path.join(APP_ROOT, '../static')  # 设置一个专门的类似全局变量的东西


class Query:
    def __init__(self, key, table, column, sql=None):
        # 打印开关

        self.DEBUG_FLAG = False

        # 数据集路径
        self.NEWS_DATA_FILE = "NewsData.csv"

        self.readPath = os.path.join(APP_STATIC_TXT, 'stop_words.txt')

        # 停用词
        self.global_stopwords = []

        self.key = key
        self.table = table
        self.column = column
        self.sql = sql

        # tfidf
        self.global_tfidf = None

        # 向量化表示
        self.global_tfidf_vec = None

        # 全局数据
        self.global_news_data = None

    # 定义删各种符号的函数
    def remove_punctuation(self, line):
        line = str(line)
        if line.strip() == '':
            return ''

        r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
        line = re.sub(r, '', line)
        return line

    # 读取停用词表
    def read_stopwords(self, stopwords_path):
        stopwords = []
        fr = codecs.open(stopwords_path, 'r', encoding='utf-8')
        for word in fr:
            stopwords.append(word.strip())

        fr.close()
        return stopwords

    # 对文本进行ETL处理，包括标点去除和分词等操作
    def text_etl_process(self, text):
        text = str(text)
        if text.strip() == '':
            return ''
        r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
        text = re.sub(r, '', text)
        text = [",".join([w for w in list(jieba.cut(text)) if w != ' '])]
        return text

    # 通过余弦相似度来匹配与特定name相似的其他n个物品,并将推荐结果返回给用户
    def recommendations(self, tfidf, tfidf_vec, news_data, text, topK):
        if self.DEBUG_FLAG:
            print("============ " + str(text) + " ===========")

        ret_news_dict = dict()

        if len(text) == 0 or len(text.strip()) == 0:
            return ret_news_dict

        # 对输入文本进行预处理
        ss = self.text_etl_process(text)

        # 获取tfidf向量化表示
        ss_vec = tfidf.transform(ss)
        if self.DEBUG_FLAG:
            print("ss            : ", ss)
            print("type(ss_vec)  : ", type(ss_vec))
            print("ss_vec        : ", ss_vec)
        cos_sim = cosine_similarity(ss_vec, tfidf_vec)
        arr = cos_sim[0]

        if self.DEBUG_FLAG:
            print("topK = ", topK)

        # print("arr ： ", arr)
        # print("-arr ： ", -arr)
        # 根据相似度排序进行截取
        idxs = list(np.argsort(-arr)[:topK])
        print(idxs)

        return idxs


    def mongodb_search(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["ancientPoetry"]
        mycol = mydb[self.table]
        a = []
        b = []
        c = []
        # str = eval("{\"type_classify\": " + "\"{}\"".format(self.typeClassify) + "}")
        for i in mycol.find(self.sql):
            a.append(i[self.column])
            c.append(i)
        return a

    # 推荐算法训练接口
    def news_recomm_train(self, data_file):
        # 加载停用词
        # mysql_search()
        self.mongodb_search()
        global_stopwords = self.read_stopwords(self.readPath)

        print("global_stopwords : ", len(global_stopwords))
        if self.DEBUG_FLAG:
            print("global_stopwords : ", global_stopwords[1000:1020])

        # data = mysql_search()
        list2 = self.mongodb_search()
        # list2 = []
        # for i in range(0, len(data)):
        #   list2.append(data[0])
        list2 = pd.Series(list2)
        print(list2)
        # 删除各种符号
        data2 = list2.apply(self.remove_punctuation)

        # 分词
        data2 = data2.apply(
            lambda x: " ".join([w for w in list(jieba.cut(x)) if w != ' ']))

        # 对切词后的cut_name字段进行向量化处理,使用sklearn的TfidfVectorizer来对文本数据进行向量化处理
        tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0).fit(data2)
        tfidf_vec = tfidf.transform(data2)
        return list2, tfidf, tfidf_vec

    def run(self):
        # 模型训练
        global_news_data, global_tfidf, global_tfidf_vec = self.news_recomm_train(self.NEWS_DATA_FILE)

        # 推荐接口
        # result_recomm = recommendations(global_tfidf, global_tfidf_vec, global_news_data,
        #                                 "Lang Sha 浪莎 800D女士舒适加厚显瘦保暖迷你绒加裆九分裤袜", 5)
        result_recomm = self.recommendations(global_tfidf, global_tfidf_vec, global_news_data,
                                             # "私募排排网数据显示，截止3月27日，股票私募仓位指数为68.35%，环比上周减仓5.23个百分点。其中，管理规模在10-20亿的私募减仓最多，环比上周仓位指数下降了14.07个百分点，一直不断加仓抄底的百亿私募也开始大幅减仓，其最新仓位指数为71.87%，环比上周下降了8.39个百分点，另外10-20亿私募减仓了8.1%个百分点，50-100亿私募减仓了7.46个百分点。具体来看，仓位在8成以上的股票私募占比降到了5成以下，近3成股票私募仓位低于5成。百亿私募方面，虽然有减仓，但整体仓位还是比较高，8成百亿私募仓位在5成以上。",
                                             # "杨靖宇，本名马尚德。1905年生于河南确山县李湾村。1923年秋考入河南省立第一工业学校。受地下党员、进步老师的影响，积极投身“五卅”运动， 1926年加入中国共产主义青年团..."
                                             self.key, 5)
        print("推荐结果:")
        print(result_recomm)
        list_all = []
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["ancientPoetry"]

        mycol = mydb[self.table]
        c = []
        result = []
        # str = eval("{\"type_classify\": " + "\"{}\"".format(self.typeClassify) + "}")
        for i in mycol.find(self.sql):
            c.append(i)
        for i in result_recomm:
            result.append(c[i])
            # print(c[i])
        return result


if __name__ == '__main__':
    sql = eval("{\"type_classify\": " + "\"{}\"".format("战争") + "}")
    test = Query("李白", "sentence", "sen_author", sql)
    result = test.run()
    print("*****************************")
    print(result)

#     #模型训练
#     global_news_data, global_tfidf, global_tfidf_vec = news_recomm_train(NEWS_DATA_FILE)
#
#     #推荐接口
#     # result_recomm = recommendations(global_tfidf, global_tfidf_vec, global_news_data,
#     #                                 "Lang Sha 浪莎 800D女士舒适加厚显瘦保暖迷你绒加裆九分裤袜", 5)
#     result_recomm = recommendations(global_tfidf, global_tfidf_vec, global_news_data,
#                                     #"私募排排网数据显示，截止3月27日，股票私募仓位指数为68.35%，环比上周减仓5.23个百分点。其中，管理规模在10-20亿的私募减仓最多，环比上周仓位指数下降了14.07个百分点，一直不断加仓抄底的百亿私募也开始大幅减仓，其最新仓位指数为71.87%，环比上周下降了8.39个百分点，另外10-20亿私募减仓了8.1%个百分点，50-100亿私募减仓了7.46个百分点。具体来看，仓位在8成以上的股票私募占比降到了5成以下，近3成股票私募仓位低于5成。百亿私募方面，虽然有减仓，但整体仓位还是比较高，8成百亿私募仓位在5成以上。",
#                                     #"杨靖宇，本名马尚德。1905年生于河南确山县李湾村。1923年秋考入河南省立第一工业学校。受地下党员、进步老师的影响，积极投身“五卅”运动， 1926年加入中国共产主义青年团..."
#                                     '王维', 5)
#     print("推荐结果:")
#     print(result_recomm)
#     list_all = []
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#     mydb = myclient["ancientPoetry"]
#
#     mycol = mydb["sentence"]
#     c = []
#     for i in mycol.find():
#         c.append(i)
#     for i in result_recomm:
#         print(c[i])
#     #print(list_all)
