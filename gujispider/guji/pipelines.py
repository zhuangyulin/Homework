# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GujiPipeline:
    def process_item(self, item, spider):
        return item


import pymysql

class GujiPipeline(object):
    def __init__(self):
        # connection database

        self.connect = pymysql.connect(host='127.0.0.1', user='root', passwd='liujiahao',
                                       db='guji')  # 后面三个依次是数据库连接名、数据库密码、数据库名称
        # get cursor
        self.cursor = self.connect.cursor()
        print("连接数据库成功")


    def process_item(self, item, spider):
        tableName = spider.name
        # sql语句
        insert_sql = """
        insert into {table} (booktitle,bookhref,brief,messagetitle) VALUES (%s,%s,%s,%s)
        """
        # insert_sql = """
        # insert into {table} (messagetitle,messagehref,message) VALUES (%s,%s,%s)
        # """
        insert_sql = insert_sql.format(table=tableName)
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['booktitle'], item['bookhref'], item['brief'], item['messagetitle']))
        # 提交，不进行提交无法保存到数据库
        self.connect.commit()
        print('存储成功')

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.connect.close()