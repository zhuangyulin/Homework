from flask import Flask, render_template
from pymongo import MongoClient
mydb = MongoClient(host='127.0.0.1').poetry
app = Flask(__name__)

@app.route('/')
def show_author():
    mytable = mydb.authors
    data1 = mytable.find_one({"auth_name": '李白'})
    data2 = mytable.find_one({"auth_name": '纳兰性德'})
    data3 = mytable.find_one({"auth_name": '陶渊明'})
    return render_template("cyf.html",result=[data1,data2,data3])

app.run(debug=True)
