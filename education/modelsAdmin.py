from flask_login import UserMixin

from sql import SQL

class Admin(UserMixin):

    
    def __init__(self):
        self.table_name = 'admins'
        self.sql = SQL()
        self.id = None
        self.account = None
        self.password = None
        self.power = None
        self.phone = None
        self.email = None
        self.info = None

    def get_account(self):
        return self.account

    def get_phone(self):
        return self.phone

    def get_email(self):
        return self.email

    def get_info(self):
        return self.info

    def get_power(self):
        return self.power

    def is_HIGH(self):
        if self.power == 'HIGH':
            return True
        else:
            return False

    def get_admin_object(self, admin_id):
        target_vector = ['id', admin_id]
        sql_result = self.sql.search_line_targetly(self.table_name, target_vector)
        try:
            self.result_to_object(sql_result)
        except:
            print('NO SUCH ADMIN.')

    def result_to_object(self, sql_result):
        # sql_result：一行数据是一个元组，整个数据是一个列表；[(-),...]
        # 从sql_result中获取数据，保存到对象中去
        if sql_result != []:
            result_tuple = sql_result[0]
            self.id = result_tuple[0]
            self.account = result_tuple[1]
            self.password = result_tuple[2]
            self.power = result_tuple[3]
            self.phone = result_tuple[4]
            self.email = result_tuple[5]
            self.info = result_tuple[6]
        else:
            pass

    def result_to_object_list(self, sql_result):
        # 从sql_result中获取数据，保存为对象列表
        admin_list = []
        if sql_result != []:
            for i in range(len(sql_result)):
                admin = Admin()
                admin.result_to_object([sql_result.pop()])
                admin_list.append(admin)
            return admin_list

    def search_all(self):
        # 搜索全部管理员，返回一个object_list
        sql_result = self.sql.search_line_all(self.table_name)
        return self.result_to_object_list(sql_result)

    def add_new_admin(self, form):
        # 在数据库中新加权限为LOW的admin
        self.id = None # id为None则数据库会自增id
        self.account = form.account.data
        self.password = form.password.data
        self.power = 'LOW'
        self.phone = form.phone.data
        self.email = form.email.data
        self.info = form.info.data

        value_list = [self.id]
        value_list.append(self.account)
        value_list.append(self.password)
        value_list.append(self.power)
        value_list.append(self.phone)
        value_list.append(self.email)
        value_list.append(self.info)

        self.sql.add_line(self.table_name, value_list)

    def update_admin_single(self, update_vector):
        # 根据一项更新admin信息
        target_vector = ['id', self.id]
        self.sql.update_line_single(self.table_name, update_vector, target_vector)

    def change_password(self, form):
        # 修改密码
        if self.verify_password(form.old_password.data):
            self.password = form.new_password.data
            update_vector = ['password', self.password]
            self.update_admin_single(update_vector)
            return True
        else:
            return False

    def change_phone(self, form):
        self.phone = form.new_phone.data
        update_vector = ['phone', self.phone]
        self.update_admin_single(update_vector)

    def change_email(self, form):
        self.email = form.new_email.data
        update_vector = ['email', self.email]
        self.update_admin_single(update_vector)

    def change_info(self, form):
        self.info = form.new_info.data
        update_vector = ['info', self.info]
        self.update_admin_single(update_vector)
    
    def delect_low_admin(self, admin_id):
        pass

    def verify_login(self, form):
        # 验证登录
        target_vector = ['account', form.account.data]
        sql_result = self.sql.search_line_targetly(self.table_name, target_vector)
        self.result_to_object(sql_result)
        return self.verify_password(form.password.data)

    def verify_password(self, password):
        # 验证密码
        if self.password == password:
            return True
        else:
            return False
