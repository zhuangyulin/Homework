
from flask import Flask
from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request
from flask.sessions import NullSession
# from flask_pyMongo import PyMongo
import pymongo
import json
from bson import json_util
 
app=Flask(__name__) #创建1个Flask实例
client = pymongo.MongoClient(host='127.0.0.1')
db =client['poetry']
collections = db.sentence

@app.route('/')
def index():
    return redirect(url_for('getdata') )

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        sname=request.form.get('sname')
    return sname

@app.route('/getdata',methods=['GET','POST'])
def getdata():
    sname=url_for('search')
    if request.method == 'POST':
        sname=request.form.get('sname')
    sentence1=collections.find_one({"sen_name":sname})
    sentence2=collections.find_one({"sen_name":'《八声甘州·摘青梅荐酒》'})
    sentence3=collections.find_one({"sen_name":'《月夜忆舍弟》'})
    sentence4=collections.find_one({"sen_name":'《寄人》'})
    sentence5=collections.find_one({"sen_name":'《别诗》'})
    sentence6=collections.find_one({"sen_name":'《小池》'})
    sentence7=collections.find_one({"sen_name":'《白头吟》'})
    return render_template('index.html',data=[sentence1,sentence2,sentence3,sentence4,sentence5,sentence6,sentence7])

if __name__ == '__main__':
    app.run(debug=True)              
