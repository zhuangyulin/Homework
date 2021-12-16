import os

import pymongo
from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask import make_response, jsonify, abort

from ancientPoetry.utils import querying
from ancientPoetry.utils.mongo import MongodbHandle
from ancientPoetry.utils.query import Query
import re
import zhon.hanzi

ind = Blueprint('index', __name__)


@ind.route('/', methods=['GET', 'POST'])
def index():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["ancientPoetry"]
    mycol = mydb["sentence"]
    result = []
    datas = []
    for i in mycol.aggregate([{"$sample": {'size': 10}}]):
        result.append(i)
    for i in result:
        poem = {}
        poem['名句'] = i['sentence']
        poem['作者名'] = i['sen_author']
        poem['诗词名'] = i['sen_name']
        poem['类型'] = i['type_classify']
        datas.append(poem)
    return render_template('recommend.html', datas=datas)

@ind.route('/author', methods=['GET', 'POST'])
def author():
    key = request.form.get('name')
    if key != None and key != "":
        que = Query(key, "poem", "作者名")
        result = que.run()
        datas = []

        for i in result:
            poem = {}
            poem['诗词名'] = i['诗词名']
            poem['作者名'] = i['作者名']
            poem['作者朝代'] = i['作者朝代']
            poetry = i['诗词'].strip('\\n')
            poetry = re.findall(zhon.hanzi.sentence, poetry)
            poem['诗词'] = poetry
            datas.append(poem)
        return render_template('authorSearch.html', datas=datas)
    else:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["ancientPoetry"]
        mycol = mydb["poem"]
        result = []
        datas = []
        for i in mycol.find().skip(10).limit(10):
            result.append(i)
        print(result)
        for i in result:
            poem = {}
            poem['诗词名'] = i['诗词名']
            poem['作者名'] = i['作者名']
            poem['作者朝代'] = i['作者朝代']
            poetry = i['诗词'].strip('\\n')
            poetry = re.findall(zhon.hanzi.sentence, poetry)
            poem['诗词'] = poetry
            datas.append(poem)

        return render_template("author.html", datas=datas)


# @ind.route('/author', methods=['GET', 'POST'])
# def index_author():
#     if request.method == 'POST':
#         key = request.form.get('name')
#         print("**************" + key + "***************")
#
#         if key == "":
#             return render_template('authorSearch.html')
#         que = Query(key, "poem", "作者名")
#         result = que.run()
#         datas = []
#
#         for i in result:
#             poem = {}
#             poem['诗词名'] = i['诗词名']
#             poem['作者名'] = i['作者名']
#             poetry = i['诗词'].strip('\\n')
#             poetry = re.findall(zhon.hanzi.sentence, poetry)
#             poem['诗词'] = poetry
#             datas.append(poem)
#         return render_template('authorSearch.html', datas=datas)
#     else:
#         return render_template('authorSearch.html')


@ind.route('/poem', methods=['GET', 'POST'])
def poem():
    key = request.form.get('name')
    if key != None and key != "":
        # return redirect('/poemSearch')
        # return render_template("poemSearch.html")
        que = Query(key, "poem", "诗词")
        result = que.run()
        datas = []

        for i in result:
            poem = {}
            poem['诗词名'] = i['诗词名']
            poem['作者名'] = i['作者名']
            poem['作者朝代'] = i['作者朝代']
            poetry = i['诗词'].strip('\\n')
            poetry = re.findall(zhon.hanzi.sentence, poetry)
            poem['诗词'] = poetry
            datas.append(poem)
        return render_template('poemSearch.html', datas=datas)
    else:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["ancientPoetry"]
        mycol = mydb["poem"]
        result = []
        datas = []
        for i in mycol.find().limit(10):
            result.append(i)
        print(result)
        for i in result:
            poem = {}
            poem['诗词名'] = i['诗词名']
            poem['作者名'] = i['作者名']
            poem['作者朝代'] = i['作者朝代']
            poetry = i['诗词'].strip('\\n')
            poetry = re.findall(zhon.hanzi.sentence, poetry)
            poem['诗词'] = poetry
            datas.append(poem)

        return render_template("poem.html", datas=datas)


# @ind.route('/poemSearch', methods=['GET', 'POST'])
# def poem_search():
#     key = request.form.get('name')
#
#     print("**************" + key + "***************")
#
#     if key == "":
#         return render_template('poemSearch.html')
#     que = Query(key, "poem", "诗词")
#     result = que.run()
#     datas = []
#
#     for i in result:
#         poem = {}
#         poem['诗词名'] = i['诗词名']
#         poem['作者名'] = i['作者名']
#         poetry = i['诗词'].strip('\\n')
#         poetry = re.findall(zhon.hanzi.sentence, poetry)
#         poem['诗词'] = poetry
#         datas.append(poem)
#     return render_template('poemSearch.html', datas=datas)


@ind.route('/poem_ci', methods=['GET', 'POST'])
def poem_ci():
    key = request.form.get('name')
    if key != None and key != "":
        que = Query(key, "ci", "诗词")
        result = que.run()
        datas = []

        for i in result:
            poem = {}
            poem['诗词名'] = i['诗名']
            poem['作者名'] = i['作者名']
            poem['作者朝代'] = i['作者朝代']
            poetry = i['诗词'].strip('\\n')
            poetry = re.findall(zhon.hanzi.sentence, poetry)
            poem['诗词'] = poetry
            datas.append(poem)
        return render_template('poem_ciSearch.html', datas=datas)
    else:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["ancientPoetry"]
        mycol = mydb["ci"]
        result = []
        datas = []
        for i in mycol.find().limit(10):
            result.append(i)
        print(result)
        for i in result:
            poem = {}
            poem['诗词名'] = i['诗名']
            poem['作者名'] = i['作者名']
            poem['作者朝代'] = i['作者朝代']
            poetry = i['诗词'].strip('\\n')
            poetry = re.findall(zhon.hanzi.sentence, poetry)
            poem['诗词'] = poetry
            datas.append(poem)

        return render_template("poem_ci.html", datas=datas)

# @ind.route('/poem_ci', methods=['GET', 'POST'])
# def index_poem_ci():
#     if request.method == 'POST':
#         key = request.form.get('name')
#         print("**************" + key + "***************")
#
#         if key == "":
#             return render_template('poem_ciSearch.html')
#         que = Query(key, "ci", "诗词")
#         result = que.run()
#         datas = []
#
#         for i in result:
#             poem = {}
#             poem['诗词名'] = i['诗名']
#             poem['作者名'] = i['作者名']
#             poetry = i['诗词'].strip('\\n')
#             poetry = re.findall(zhon.hanzi.sentence, poetry)
#             poem['诗词'] = poetry
#             datas.append(poem)
#         return render_template('poem_ciSearch.html', datas=datas)
#     else:
#         return render_template('poem_ciSearch.html')


@ind.route('/sentence', methods=['GET', 'POST'])
def sentence():
    key = request.form.get('name')
    if key != None and key != "":
        sql = eval("{\"type_classify\": " + "\"{}\"".format("战争") + "}")
        que = Query(key, "sentence", "sen_author", sql)
        result = que.run()
        datas = []

        for i in result:
            poem = {}
            poem['名句'] = i['sentence']
            poem['作者名'] = i['sen_author']
            poem['诗词名'] = i['sen_name']
            poem['类型'] = i['type_classify']
            datas.append(poem)
        return render_template('sentenceSearch.html', datas=datas)
    else:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["ancientPoetry"]
        mycol = mydb["sentence"]
        result = []
        datas = []
        for i in mycol.find().limit(10):
        # for i in mycol.aggregate([{"$sample": {'size': 1}}]):
            result.append(i)
        print(result)
        for i in result:
            poem = {}
            poem['名句'] = i['sentence']
            poem['作者名'] = i['sen_author']
            poem['诗词名'] = i['sen_name']
            poem['类型'] = i['type_classify']
            datas.append(poem)

        return render_template("sentence.html", datas=datas)


@ind.route('/recommend', methods=['GET', 'POST'])
def test():
    key = request.form.get('name')
    if key == "1":
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["ancientPoetry"]
        mycol = mydb["sentence"]
        result = []
        datas = []
        for i in mycol.aggregate([{"$sample": {'size': 5}}]):
            result.append(i)
        print(result)
        for i in result:
            poem = {}
            poem['名句'] = i['sentence']
            poem['作者名'] = i['sen_author']
            poem['诗词名'] = i['sen_name']
            poem['类型'] = i['type_classify']
            datas.append(poem)
        return render_template('recommend.html', datas=datas)
    else:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["ancientPoetry"]
        mycol = mydb["sentence"]
        result = []
        datas = []
        for i in mycol.aggregate([{"$sample": {'size': 5}}]):
            result.append(i)
        print(result)
        for i in result:
            poem = {}
            poem['名句'] = i['sentence']
            poem['作者名'] = i['sen_author']
            poem['诗词名'] = i['sen_name']
            poem['类型'] = i['type_classify']
            datas.append(poem)
        return render_template('recommend.html', datas=datas)
