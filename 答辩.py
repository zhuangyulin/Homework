# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Microsoft VS Code\Test\作业6\login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys
from lxml import etree
import pymysql
import requests
import re
import ast
import time
from pymongo import MongoClient

# import teamname
global mark
mark = 0
global liulanqi_url


class login(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 733)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        MainWindow.setFont(font)
        
        MainWindow.setStyleSheet("\n"
                                 "#MainWindow{\n"
                                 "    background: url(C:/Users/user/Desktop/1.jpg);\n"
                                 "}\n"
                                 "QFrame{\n"
                                 "background:rgba(255,255,255,0.6)\n"
                                 "}\n"
                                 "")

        self.frame = QtWidgets.QFrame(MainWindow)
        self.frame.setGeometry(QtCore.QRect(500, 220, 931, 581))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # layout()->setSizeConstraint(QLayout::SetFixedSize);
       

        self.Button_cancel = QtWidgets.QPushButton(self.frame)
        self.Button_cancel.setGeometry(QtCore.QRect(510, 450, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Button_cancel.setFont(font)
        self.Button_cancel.setObjectName("Button_cancel")
        self.lineEdit_name = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_name.setGeometry(QtCore.QRect(260, 160, 421, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.lineEdit_name.setFont(font)
        self.lineEdit_name.setStyleSheet("QLineEdit{\n"
                                         "border-color: rgba(0, 0, 0,1);\n"
                                         "}")
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.checkBox = QtWidgets.QCheckBox(self.frame)
        self.checkBox.setGeometry(QtCore.QRect(410, 390, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.checkBox.setTristate(False)
        self.checkBox.setObjectName("checkBox")
        self.lineEdit_password = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_password.setGeometry(QtCore.QRect(260, 305, 421, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.lineEdit_password.setFont(font)
        self.lineEdit_password.setText("")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.Button_login = QtWidgets.QPushButton(self.frame)
        self.Button_login.setGeometry(QtCore.QRect(240, 450, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Button_login.setFont(font)
        self.Button_login.setObjectName("Button_login")
        self.textEdit_2 = QtWidgets.QTextEdit(self.frame)
        self.textEdit_2.setGeometry(QtCore.QRect(210, 146, 511, 71))
        self.textEdit_2.setStyleSheet("QTextEdit{\n"
                                      "border-radius:15px;\n"
                                      "background:rgba(255,255,255,1)\n"
                                      "\n"
                                      "}\n"
                                      "")
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setAcceptRichText(True)
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.frame)
        self.textEdit_3.setGeometry(QtCore.QRect(210, 286, 511, 71))
        self.textEdit_3.setStyleSheet("QTextEdit{\n"
                                      "border-radius:15px;\n"
                                      "background:rgba(255,255,255,1)\n"
                                      "\n"
                                      "}\n"
                                      "")
        self.textEdit_3.setReadOnly(True)
        self.textEdit_3.setObjectName("textEdit_3")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(100, 60, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel\n"
                                 "{\n"
                                 "color:#000;\n"
                                 "background:transparent;\n"
                                 "}")
        self.label.setObjectName("label")
        self.textEdit_3.raise_()
        self.textEdit_2.raise_()
        self.Button_cancel.raise_()
        self.lineEdit_name.raise_()
        self.checkBox.raise_()
        self.lineEdit_password.raise_()
        self.Button_login.raise_()
        self.label.raise_()
        self.retranslateUi(MainWindow)
        self.Button_cancel.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.showMaximized()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "诗词demo测试 ----v1.0.0"))
        self.Button_cancel.setText(_translate("MainWindow", "取消"))
        self.lineEdit_name.setPlaceholderText(_translate("MainWindow", "UserName"))
        self.checkBox.setText(_translate("MainWindow", "记住密码"))
        self.lineEdit_password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.Button_login.setText(_translate("MainWindow", "登录"))
        self.label.setText(_translate("MainWindow", "古诗文-登录"))


class NewWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.initUI()
        # def initUI(self):
        # 设置窗口标题和大小
        # self.showMaximized()
        self.setWindowTitle('数据库测试')
        self.resize(2100, 1100)
        
                                 


        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(1000, 0, 1000, 1100))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("background: url(C:/Users/user/Desktop/2.png);")
        

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(1020, 300, 560, 600))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.hide()

        self.lineEdit_search2 = QTextEdit(self)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.lineEdit_search2.setStyleSheet("border:none")
        self.lineEdit_search2.setFont(font)
        self.lineEdit_search2.setObjectName("lineEdit_search")
        self.lineEdit_search2.setGeometry(1100, 350, 700, 550)
        self.lineEdit_search2.setStyleSheet("background:rgba(0,0,0,0.1)")
        self.lineEdit_search2.setReadOnly(True)
        # self.lineEdit_search2.setStyleSheet("border:solid")
        


        self.Button_show = QtWidgets.QPushButton(self)
        self.Button_show.setGeometry(QtCore.QRect(1220, 200, 120, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Button_show.setFont(font)
        self.Button_show.setObjectName("Button_show")
        self.Button_show.setEnabled(True)
        self.Button_show.setText("显示")

        self.Button_notshow = QtWidgets.QPushButton(self)
        self.Button_notshow.setGeometry(QtCore.QRect(1535, 200, 120, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Button_notshow.setFont(font)

        self.Button_notshow.setObjectName("Button_notshow")
        self.Button_notshow.setText("清除")
        self.Button_spy = QtWidgets.QPushButton(self)
        self.Button_spy.setGeometry(QtCore.QRect(1570, 200, 120, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Button_spy.setFont(font)
        self.Button_spy.setObjectName("Button_spy")
        self.Button_spy.setText("爬取")

        self.Button_spy.hide()

        self.comboBox = QComboBox(self)

        # self.comboBox.hide()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.addItem("作者名")
        self.comboBox.addItem("诗词名")
        self.comboBox.addItem("诗词")
        self.comboBox.addItem("作者朝代")
        self.comboBox.addItem("注释译文及赏析")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(1150, 100, 260, 35))
        self.lineEdit_search = QLineEdit(self)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.lineEdit_search.setFont(font)
        self.lineEdit_search.setObjectName("lineEdit_search")
        _translate = QtCore.QCoreApplication.translate
        self.lineEdit_search.setPlaceholderText(_translate("MainWindow", "search"))
        # self.lineEdit_search.hide()

        self.lineEdit_search.setGeometry(QtCore.QRect(1470, 100, 260, 35))
        self.lineEdit_search1 = QLineEdit(self)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.lineEdit_search1.setFont(font)
        self.lineEdit_search1.setObjectName("lineEdit_search")

        self.lineEdit_search1.hide()

        self.lineEdit_search1.setGeometry(QtCore.QRect(1330, 150, 250, 30))

        self.centralwidget = QtWidgets.QWidget(self)
        self.browser = QWebEngineView(self.centralwidget)
        self.browser.setGeometry(QtCore.QRect(0, 0, 1000, 1000))  # (50 左边, 50 右边, 700 宽, 500 高)
        # self.newwindow.showMaximized()
        self.setCentralWidget(self.centralwidget)
        ###使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))
        # 添加导航栏到窗口中
        self.addToolBar(navigation_bar)

        self.centralwidget.lower()

        # timer = QTimer() # 计时器
        # timer.timeout.connect(self.dongtai)

        # thread = MyThread() # 创建一个线程
        # thread.sec_changed_signal.connect(self.dongtai) # 线程发过来的信号挂接到槽：update
        # self.Button_spy.clicked.connect(lambda :thread.start())

        # QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction('30只球队分析', self)
        next_button = QAction('足彩胜利分析', self)
        stop_button = QAction('足彩平局分析', self)
        reload_button = QAction('足彩失败分析', self)
        football_button = QAction('足彩首页', self)
        caipiao_button = QAction('足彩彩票页', self)

        back_button.triggered.connect(self.new_picture1)
        next_button.triggered.connect(self.new_picture4)
        stop_button.triggered.connect(self.new_picture3)
        reload_button.triggered.connect(self.new_picture2)
        football_button.triggered.connect(self.new_picture5)
        caipiao_button.triggered.connect(self.new_picture6)

        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)
        navigation_bar.addAction(football_button)
        navigation_bar.addAction(caipiao_button)

        # 添加URL地址栏
        liulanqi_url = "http://zx.500.com/zc/lsdz.php?lotid=1"
        self.browser.setUrl(QUrl(liulanqi_url))
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        # 让浏览器相应url地址的变化
        self.browser.urlChanged.connect(self.renew_urlbar)

        # thread = MyThread() # 创建一个线程
        # thread.sec_changed_signal.connect(self.dongtai) # 线程发过来的信号挂接到槽：update
        # self.Button_spy.clicked.connect(lambda :thread.start())
        # # btn2.clicked.connect(lambda :thread.terminate()) # 线程中止# 线程中止

    def dongtai(self, sec):
        self.tableWidget.clear()
        sql = 'select * from color_lottery'
        conn = pymysql.connect(host='localhost', port=3306, user='root', password="Cqq@123", db="bigdata")
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        result = list(result)
        titles = ['期号', '结果', '最高可得奖金', '最低可得奖金', '3的个数', '1的个数', '0的个数']
        row = cur.rowcount  # 取得记录个数，用于设置表格的行数
        row = int(row)
        # if mark==1:
        #     row=int(row/2)
        vol = len(result[0])  # 取得字段数，用于设置表格的列数
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(vol)
        self.tableWidget.setHorizontalHeaderLabels(titles)
        for i in range(row):
            for j in range(vol):
                temp_data = result[i][j]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.tableWidget.setItem(i, j, data)
            self.tableWidget.update()
            self.tableWidget.viewport().update()

    def spy_data(self):
        class Color_lottery():
            def __init__(self):
                self.base_url = "http://datachart.500.com/sfc/hmfb.shtml"
                self.headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}

            def list_of_groups(self, list_info, per_list_len):
                list_of_group = zip(*(iter(list_info),) * per_list_len)
                end_list = [list(i) for i in list_of_group]  # i is a tuple
                count = len(list_info) % per_list_len
                end_list.append(list_info[-count:]) if count != 0 else end_list
                return end_list

            def get_main_datas(self):
                html = requests.get(self.base_url, headers=self.headers)
                html.encoding = "utf-8"
                content = etree.HTML(html.content)
                if content != "":
                    contents = content.xpath("//table[@class='sfc-tb-a']//tr//td//text()")
                return contents

            def parse_main_datas(self):
                content = self.get_main_datas()
                datalist = self.list_of_groups(content, 8)
                datalists = str(datalist).replace("\' \', ", "")
                datalist_source = re.findall(r"'21061'.*?(?='显示全部')", datalists)
                datalists_source = str(datalist_source).replace(", \"", "").replace("\"", "").replace(", []", "")
                result = [datalists_source]
                results = str(result).replace("\"", "")
                # 将str类型的
                result_source = ast.literal_eval(results)
                return result_source

            def create_table(self):
                flag = False
                # sql语句定义表的属性
                sql1 = " DROP TABLE IF EXISTS color_lottery"
                sql = """
                    CREATE TABLE IF NOT EXISTS color_lottery( 
                        `issume_num` varchar(255) default NULL,
                        `lottery_num` varchar(255) default NULL,
                        `fir_bonus` varchar(255) default NULL,
                        `sec_bonus` varchar(255) default NULL, 
                        `3_num` varchar(255) default NULL,
                        `1_num` varchar(255) default NULL,
                        `0_num` varchar(255) default NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                    """
                # 创建和数据库的链接
                db = pymysql.connect(host='localhost', user="root", password='wwwlovecom@', port=3306,
                                     database="bigdata")
                cursor = db.cursor()
                # 执行sql语句
                try:
                    cursor.execute(sql1)
                    cursor.execute(sql)
                    # 提交数据
                    db.commit()
                    print("数据表创建成功")
                    flag = True
                except Exception as e:
                    # 回滚数据
                    db.rollback()
                    print("数据表创建失败")
                    flag = False
                finally:
                    # 关闭连接
                    cursor.close()
                    db.close()
                return flag

            def write_data_to_databases(self):
                # 创建和数据库的链接
                db = pymysql.connect(host='localhost', user='root', password='wwwlovecom@', database='bigdata')
                cursor = db.cursor()
                datalist = self.parse_main_datas()
                print(datalist)
                for i in datalist:
                    print(i)
                    if len(i) != 7:
                        continue
                    sql = "insert into color_lottery values('%s','%s','%s','%s','%s','%s','%s')" % (
                    i[0], i[1], i[2], i[3], i[4], i[5], i[6])
                    try:
                        if cursor.execute(sql):
                            print("执行插入成功")
                            db.commit()
                    except Exception as e:
                        print("执行失败")
                        print(e)
                        db.rollback()
                cursor.close()
                db.close()
                print("存储完成")

                msg_box = QMessageBox(QMessageBox.Warning, '提示', '存储完成')
                msg_box.exec_()

            def run(self):
                self.parse_main_datas()
                self.create_table()
                self.write_data_to_databases()

        if __name__ == "__main__":
            self.show_data()
            js = Color_lottery()
            js.run()

    def cancel_data(self):
        self.lineEdit_search2.clear()

    def show_data(self):
        import pymongo
        from bson import json_util as jsonb
        mark = 0
        self.tableWidget.clear()
        # heigherdata=self.lineEdit_search1.text()
        data11 = self.comboBox.currentText()
        data111 = self.lineEdit_search.text()
        # print(data111)
        # print(heigherdata)
        client = pymongo.MongoClient(host='127.0.0.1')
        db = client['poetry']
        collections = db.poem
        if data11 == '作者名':
            result1 = db.poem.find({"作者名": data111}, {"作者名": 1, "诗词名": 1, "诗词": 1, "作者朝代": "1", "注释译文及赏析": 1, '_id': 0})
        elif data11 == '诗词名':
            result1 = db.poem.find({"诗词名": data111}, {"作者名": 1, "诗词名": 1, "诗词": 1, "作者朝代": "1", "注释译文及赏析": 1, '_id': 0})
        elif data11 == '诗词':
            result1 = db.poem.find({"诗词": data111}, {"作者名": 1, "诗词名": 1, "诗词": 1, "作者朝代": "1", "注释译文及赏析": 1, '_id': 0})
        elif data11 == '作者朝代':
            result1 = db.poem.find({"作者朝代": data111},
                                   {"作者名": 1, "诗词名": 1, "诗词": 1, "作者朝代": "1", "注释译文及赏析": 1, '_id': 0})
        elif data11 == '注释译文及赏析':
            result1 = db.poem.find({"注释译文及赏析": data111},
                                   {"作者名": 1, "诗词名": 1, "诗词": 1, "作者朝代": "1", "注释译文及赏析": 1, '_id': 0})

        # result1 = db.author.find({"作者名": "[李白]"},{"诗词":1,'_id':0})
        result = list(result1)
        # print(result)

        if len(result) == 0:
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '查询为空')
            msg_box.exec_()
        else:
            # row=len(result)  #取得记录个数，用于设置表格的行数
            # row=int(row)
            # if mark==1:
            #     row=int(row/2)
            # vol=len(result[0])  #取得字段数，用于设置表格的列数
            # self.tableWidget.setRowCount(row)
            # self.tableWidget.setColumnCount(vol)
            # self.tableWidget.setHorizontalHeaderLabels(titles)
            result = str(result)
            result = result.replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace('"',
                                                                                                        "").replace(
                "\\r", "").replace("'", "").replace("  ", "").replace("\\", "").replace("\\u3000", "").replace("n",
                                                                                                               "\n ").replace(
                ",", "  ")
            result = result.replace("u3000", "")
            # print(result)
            self.lineEdit_search2.setText(result)

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def new_picture1(self):
        # 设置浏览器
        self.centralwidget = QtWidgets.QWidget(self)
        self.browser = QWebEngineView(self.centralwidget)
        self.browser.setGeometry(QtCore.QRect(0, 0, 1000, 900))  # (50 左边, 50 右边, 700 宽, 500 高)
        # self.setCentralWidget(self.centralwidget)
        # self.browser = QWebEngineView()
        liulanqi_url = "file:///C:/Microsoft VS Code/Test/答辩/zhuzhuang.html"
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(liulanqi_url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.lower()

    def new_picture2(self):
        # 设置浏览器
        self.centralwidget = QtWidgets.QWidget(self)
        self.browser = QWebEngineView(self.centralwidget)
        self.browser.setGeometry(QtCore.QRect(0, 0, 1000, 900))  # (50 左边, 50 右边, 700 宽, 500 高)
        # self.setCentralWidget(self.centralwidget)
        # self.browser = QWebEngineView()
        liulanqi_url = "file:///C:/Microsoft VS Code/Test/答辩/bingzhuang1.html"
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(liulanqi_url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.lower()

    def new_picture3(self):
        # 设置浏览器
        self.centralwidget = QtWidgets.QWidget(self)
        self.browser = QWebEngineView(self.centralwidget)
        self.browser.setGeometry(QtCore.QRect(0, 0, 1000, 900))  # (50 左边, 50 右边, 700 宽, 500 高)
        # self.setCentralWidget(self.centralwidget)
        # self.browser = QWebEngineView()
        liulanqi_url = "file:///C:/Microsoft VS Code/Test/答辩/bingzhuang2.html"
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(liulanqi_url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.lower()

    def new_picture4(self):
        # 设置浏览器
        self.centralwidget = QtWidgets.QWidget(self)
        self.browser = QWebEngineView(self.centralwidget)
        self.browser.setGeometry(QtCore.QRect(0, 0, 1000, 900))  # (50 左边, 50 右边, 700 宽, 500 高)
        # self.setCentralWidget(self.centralwidget)
        # self.browser = QWebEngineView()
        liulanqi_url = "file:///C:/Microsoft VS Code/Test/答辩/bingzhuang3.html"
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(liulanqi_url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.lower()

    def new_picture5(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.browser = QWebEngineView(self.centralwidget)
        self.browser.setGeometry(QtCore.QRect(0, 0, 1000, 900))  # (50 左边, 50 右边, 700 宽, 500 高)
        # self.setCentralWidget(self.browser)
        # 设置浏览器
        # self.browser = QWebEngineView()
        liulanqi_url = "http://zx.500.com/zc/lsdz.php?lotid=1"
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(liulanqi_url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.lower()

    def new_picture6(self):
        # 设置浏览器
        # self.browser = QWebEngineView()
        self.centralwidget = QtWidgets.QWidget(self)
        self.browser = QWebEngineView(self.centralwidget)
        self.browser.setGeometry(QtCore.QRect(0, 0, 1000, 900))  # (50 左边, 50 右边, 700 宽, 500 高)
        liulanqi_url = "http://datachart.500.com/sfc/hmfb.shtml"
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(liulanqi_url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.lower()


if __name__ == '__main__':
    import sys
    import pymysql

    # 建立数据库连接
    # dbconn = pymysql.connect(host='localhost',user="root",password="wwwlovecom@",port=3306,db="test")
    app = QtWidgets.QApplication(sys.argv)
    main = NewWindow()
    # main.window.showMaximized()
    # timer = QTimer() # 计时器
    # timer.timeout.connect(main.show_data)
    widget = QtWidgets.QMainWindow()
    # widget.window.showMaximized()
    # widget=QtWidgets.QWidget()
    ui = login()  # 这里改成你自己的项目名称，如果你没特意改过，就默认就行
    ui.setupUi(widget)
    widget.show()


    # main.show()

    def db_login():
        user_name = ui.lineEdit_name.text()
        user_pwd = ui.lineEdit_password.text()
        sql = "select * from user where username='%s' and password='%s'" % (user_name, user_pwd)
        conn = pymysql.connect(host='localhost', port=3306, user='root', password="Cqq@123", db="test")
        cur = conn.cursor()
        if len(user_name) == 0 or len(user_pwd) == 0:
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '您的用户名或密码不能为空')
            msg_box.exec_()
        else:
            try:
                cur.execute(sql)
                result = cur.fetchall()
                num = len(result)
                # print(num)
                if num == 1:
                    # msg_box = QMessageBox(QMessageBox.Warning, '提示', '登录成功')
                    # msg_box.exec_()
                    cur.close()
                    conn.close()
                    widget.close()
                    main.show()
                else:
                    # qw.QMessageBox.information(self.MainWindow, '消息',
                    # "用户名或密码错误")
                    msg_box = QMessageBox(QMessageBox.Warning, '提示', '用户名或密码错误')
                    msg_box.exec_()
            except:
                conn.rollback()


    ui.Button_login.clicked.connect(db_login)
    username = ui.lineEdit_name.text()
    password = ui.lineEdit_password.text()
    main.Button_show.clicked.connect(main.show_data)
    main.Button_notshow.clicked.connect(main.cancel_data)
    main.Button_spy.clicked.connect(main.spy_data)
    sys.exit(app.exec_())
