from flask import Flask
from flask import render_template #渲染
from pymongo import MongoClient
from flask_pymongo import PyMongo
from gevent import pywsgi

app = Flask(__name__)
app.config['DEBUG'] = True  # 开启 debug
mydb = MongoClient(host='127.0.0.1').bencao  # 开启数据库实例

@app.route('/') #主页地址,“装饰器”
def index():
    mytable=mydb.about_phrase
    type1=mytable.find({"成语类型":'季节成语'})
    type2=mytable.find({"成语类型":'天气成语'})
    type3=mytable.find({"成语类型":'生肖成语'})
    type4=mytable.find({"成语类型":'人物成语'})
    # return render_template('cyftest.html',result=type1)
    return render_template('index.html',type1=type1,type2=type2,type3=type3,type4=type4)#把index.html文件读进来，再交给浏览器 

app.run(debug=True)
