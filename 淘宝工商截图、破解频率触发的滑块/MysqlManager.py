# -*- coding: utf-8 -*-
# Author: wangkun
# Date: 2022-04-25 16:59:12
# LastEditTime: 2022-04-29 16:31:18
# LastEditors: wkun
# FilePath: /nfswork/code/MysqlManager.py
# Description:


# import MysqlManager as MY
#
# mysql = MY.MysqlManager('yzyt','root','Men6862471', host='localhost', port=3306, charset='utf8', use_unicode=True)
# 插入
# INSERT INTO tablename(列名…) VALUES('列值');  f"INSERT INTO SF(num_name)VALUES('{num}');"
# mysql.insert("INSERT INTO globalsources" + str(tuple(dit.keys())).replace("'","") + f"VALUES{tuple(dit.values())};")
# 更新
# mysql.update(
#         "UPDATE madeinchina SET sales" + f"='{dit['sales']}' WHERE id={i};")
# 查询
# mysql.get('select href from madeinchina where num=1;',get_one=True)
import pymysql


class MysqlManager(object):
    '''mysql管理器'''

    def __init__(self, db, user, passwd, host='localhost', port=3306, charset='utf8', use_unicode=True):
        '''初始化数据库'''
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port
        self.charset = charset
        self.connect = None
        self.cursor = None

    def connect_db(self):
        """
            dbManager.connect_db()
        连接数据库
        """
        params = {"db": self.db, "user": self.user, "passwd": self.passwd, "host": self.host, "port": self.port, "charset": self.charset}
        self.connect = pymysql.connect(**params)
        self.cursor = self.connect.cursor()

    def close_db(self):
        '''
            dbManager.close_db()
        关闭数据库
        '''
        self.cursor.close()
        self.connect.close()

    def insert(self, sql):
        '''
            dbManager.insert(table, insert_data)
        添加数据到数据库
        '''
        # 用户传入数据字典列表数据，根据key, value添加进数据库
        # 连接数据库
        self.connect_db()

        try:
            self.cursor.execute(sql.replace("'None'", "NULL").replace("None", "NULL"))
            self.connect.commit()
        except Exception as error:
            print(error)
        finally:
            self.close_db()

    def insert_large(self,sql):
        '''
            大数据插入
        :param sql:
        :return:
        '''
        try:
            self.cursor.execute(sql.replace("'None'", "NULL").replace("None", "NULL"))
            self.connect.commit()
        except Exception as error:
            print(error)
            self.close_db()
        finally:
            pass

    def delete(self, sql):
        '''
            dbManager.delete(sql)
        删除数据库中的数据
        '''
        self.connect_db()
        self.cursor.execute(sql.replace("'None'", "NULL").replace("None", "NULL"))
        self.connect.commit()
        self.close_db()

    def update(self, sql):
        """
            dbManager.update(sql)
        更新数据
        """
        self.connect_db()

        # 处理传入的数据
        self.cursor.execute(sql.replace("'None'", "NULL").replace("None", "NULL"))
        self.connect.commit()
        self.close_db()

    def get(self, sql, get_one=False):
        """
            dbManager.get(sql, [get_one]) -> tupel
        获取数据 返回一个元祖

        """
        self.connect_db()

        # 处理显示的数据
        self.cursor.execute(sql.replace("'None'", "NULL").replace("None", "NULL"))

        # 返回一条数据还是所有数据
        if get_one:
            result = self.cursor.fetchone()
        else:
            result = self.cursor.fetchall()
        self.close_db()
        return result
