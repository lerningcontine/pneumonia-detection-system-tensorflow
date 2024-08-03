import pymysql


class DB:
    """用户信息管理系统数据模型"""

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='123456', database='Category', charset='utf8')
        self.cursor = self.conn.cursor()

    def all_user(self):
        """返回所有的用户数据"""
        sql = 'select * from user_informations'
        self.cursor.execute(sql)
        self.students = self.cursor.fetchall()
        return self.students

    def all_cate(self):
        """返回所有的分类数据"""
        sql = 'select * from Cate'
        self.cursor.execute(sql)
        self.cates = self.cursor.fetchall()
        return self.cates

    def check_login(self, username, password):
        sql = 'select * from user_informations'
        self.cursor.execute(sql)
        self.users = self.cursor.fetchall()
        # print(self.users)
        for user in self.users:
            # print(user[0], user[1])
            if username == user[0] and password == user[1]:
                return True
        return False

    def insert(self, information):
        """将数据插入到列表"""
        informations = self.all_user()
        for i in informations:
            if i[0] == information['user_sco']:
                return False

        sql = f'INSERT INTO user_informations (user_sco, password, name, address, sex, number) VALUES ("{information["user_sco"]}", "{information["user_passwd"]}","{information["name"]}","{information["address"]}","{information["sex"]}","{information["number"]}");'
        self.cursor.execute(sql)
        self.conn.commit()
        return True

    def insert_cate(self, information):
        """将识别后的结果数据插入到列表"""
        sql = f'INSERT INTO Cate (user_sco, class, img_parh) VALUES ("{information["user_sco"]}", "{information["result"]}","{information["path"]}");'
        self.cursor.execute(sql)
        self.conn.commit()
        return True

    def delete(self, user_sco):
        """根据用户号获取用户数据，如果没有就返回 False"""
        # 因存在外键关系，用户进行的分类任务，如果需要删除用户，应需要先删除用户分类的所有任务
        cates = self.all_cate()
        for item in cates:
            if item[0] == user_sco:
                sql = f"DELETE FROM Cate WHERE user_sco = '{user_sco}'"
                self.cursor.execute(sql)
                self.conn.commit()

        users = self.all_user()
        for user in users:
            if user_sco == user[0]:
                sql = f"DELETE FROM user_informations WHERE user_sco = '{user_sco}'"
                self.cursor.execute(sql)
                self.conn.commit()
                break
        else:
            return False
        return True

    def delect_cate(self, cate_path):
        sql = f"DELETE FROM Cate WHERE img_parh = '{cate_path}'"
        self.cursor.execute(sql)
        self.conn.commit()
        return True


    def change_user(self, information):
        """更新用户信息"""
        sql = f"UPDATE user_informations SET password = '{information['user_passwd']}'," \
                      f" name = '{information['name']}', sex = '{information['sex']}', address = '{information['address']}', " \
                      f"number = '{information['number']}' where user_sco = '{information['user_sco']}'"
        self.cursor.execute(sql)
        self.conn.commit()
        return True

    def change_cate(self, information):
        """更新用户信息"""
        sql = "UPDATE Cate SET class = %s WHERE img_parh = %s and user_sco = %s"
        self.cursor.execute(sql, (information['class_'], information['old_path'], information['user_sco']))
        self.conn.commit()
        return True


db = DB()
# print(db.all_cate())