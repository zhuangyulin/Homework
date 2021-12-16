
from flask import Flask
from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request
from flask.sessions import NullSession
# from flask_pyMongo import PyMongo
import pymongo
 
app=Flask(__name__) #创建1个Flask实例
client = pymongo.MongoClient(host='127.0.0.1')
db =client['poetry']
collections = db.users

@app.route('/')
def index():
    return redirect( url_for('login') )

#登录页面
@app.route('/user_login')
def user_login():
    return render_template('login.html')

#获取注册请求及处理
@app.route('/register',methods=['GET','POST'])
def getRigistRequest():
    if request.method == 'GET':
        return render_template('注册.html')
    if request.method == 'POST':
        userId=request.form.get('userId')
        password=request.form.get('password')
        phone=request.form.get('phone')
        email=request.form.get('email')
        user=collections.find({"userId":userId,"password":password})
        if str(user.count())!='0':
            return '已有账号请直接登录'
        else:
            collections.insert({"userId":userId,"password":password,"phone":phone,"email":email})
    return render_template('login.html')

#获取登录请求及处理
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        userId=request.form.get('userId')
        password=request.form.get('password')
        user=collections.find({"userId":userId,"password":password})
        t=str(user.count())
        if str(user.count())=='0':
            return '用户名或密码登录失败，请返回重新登录，没有账号请先注册'
    return render_template('index1.html')

# @app.route('/search',methods=['GET','POST'])
# def search():
#     if request.method == 'POST':
#         sname=request.form.get('sname')
#     return sname

# @app.route('/getdata',methods=['GET','POST'])
# def getdata():
#     # sname=url_for('search')
#     if request.method == 'POST':
#         sname=request.form.get('sname')
#     sentence1=collections.find_one({"sen_name":sname})
#     sentence2=collections.find_one({"sen_name":'《大林寺桃花》'})
#     sentence3=collections.find_one({"sen_name":'《水调歌头·游览》'})
#     return render_template('index.html',data=[sentence1,sentence2,sentence3])

        
if __name__ == '__main__':
    app.run(debug=True)              #启动socket
