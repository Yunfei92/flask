import sqlite3

# Data structure:
# some_vector:[column_name, value]
# some_list:[value, value, ...]

class SQL(object):


    def __init__(self):
        self.db_name = 'wenhua.db'
        self.conn = sqlite3.connect(self.db_name, isolation_level=None) # 自动commit()
        self.cursor = self.conn.cursor()
        self.db_init()
        
    def db_init(self):
        # 数据库初始化，建立各种表格
        cmd_table_articles = '''
            CREATE TABLE IF NOT EXISTS articles
            (
                id              TEXT    PRIMARY KEY     NOT NULL,
                title           TEXT,
                author          TEXT,
                tag             TEXT,
                flag            TEXT,
                create_time     TEXT,
                update_time     TEXT,
                txt_markdown    TEXT,
                txt_html        TEXT,
                reading_times   INTEGER,
                admin_id        INTEGER,
                FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE NO ACTION
            );
        '''
        cmd_table_admins = '''
            CREATE TABLE IF NOT EXISTS admins
            (
                id              INTEGER     PRIMARY KEY     NOT NULL,
                account         TEXT,
                password        TEXT,
                power           TEXT,
                phone           TEXT,
                email           TEXT,
                info            TEXT
            );
        '''
        cmd_table_indexs = '''
            CREATE TABLE IF NOT EXISTS indexs
            (
                id              INTEGER     PRIMARY KEY     NOT NULL,
                name            TEXT,
                article_id      TEXT
            );
        '''
        index_init_value_list_1 = (None, 'website_info', None)
        index_init_value_list_2 = (None, 'update_info', None)
        index_init_value_list_3 = (None, 'index_imax', None)
        index_init_value_list_4 = (None, 'notice_board', None)

        admin_init_value_list_1 = (None, 'admin', '******', 'HIGH', None, None, None)

        try:
            self.cursor.execute(cmd_table_articles)
            self.cursor.execute(cmd_table_admins)
            self.cursor.execute(cmd_table_indexs)
            print('CREATE TABLE SUCCESS.')
            if self.search_line_all('indexs') == []:
                self.add_line('indexs', index_init_value_list_1)
                self.add_line('indexs', index_init_value_list_2)
                self.add_line('indexs', index_init_value_list_3)
                self.add_line('indexs', index_init_value_list_4)
                print('INIT INDEXS SUCCESS')
            if self.search_line_all('admins') == []:
                self.add_line('admins', admin_init_value_list_1)
                print('INIT ADMINS SUCCESS')
            else:
                pass
        except:
            print('CREATE TABLE FAILED.')
            return False

    def add_line(self, table_name, value_list):
        # 根据全属性值添加一行数据
        # INSERT INTO VALUES (?,?,?,...),(value1,value2,value3,...,) # 注意最后一项必须带逗号
        cmd_part = ['INSERT']
        cmd_part.append('INTO')
        cmd_part.append(str(table_name))
        cmd_part.append('VALUES')
        cmd_part.append('(')
        cmd_part.append(','.join(['?'] * len(value_list))) # 占位符部分
        cmd_part.append(')')
        step = ' ' # 空格
        cmd_add_line = step.join(cmd_part)
        try:
            self.cursor.execute(cmd_add_line, value_list) # 采用占位符的方式执行语句
            print('ADD LINE SUCCESS.')
        except:
            print('ADD LINE FAILED.')
        
    def update_line_part(self, table_name, column_list, value_list, target_vector):
        # 根据部分属性更新一行数据
        cmd_part = ['UPDATE']
        cmd_part.append(str(table_name))
        cmd_part.append('SET')
        for i in range(len(column_list)):
            if i != 0:
                cmd_part.append(',')
            cmd_part.append(str(column_list.pop(0)))
            cmd_part.append('=')
            cmd_part.append('?')
        cmd_part.append('WHERE')
        cmd_part.append(str(target_vector.pop(0)))
        cmd_part.append('=')
        cmd_part.append('?')
        step = ' '
        cmd_update_line = step.join(cmd_part)
        try:
            value_list.extend(target_vector) # 合并2个列表剩余的部分
            self.cursor.execute(cmd_update_line, value_list) # 同样采用占位符的方式来防止sql注入
            print('UPDATE LINE PART SUCCESS.')
        except:
            print('UPDATE LINE PART FAILED.')

    def update_line_single(self, table_name, value_vector, target_vector):
        # 根据单一属性更新一行数据
        cmd_part = ['UPDATE']
        cmd_part.append(str(table_name))
        cmd_part.append('SET')
        cmd_part.append(str(value_vector.pop(0)))
        cmd_part.append('=')
        cmd_part.append('?')
        cmd_part.append('WHERE')
        cmd_part.append(str(target_vector.pop(0)))
        cmd_part.append('=')
        cmd_part.append('?')
        step = ' '
        cmd_update_line = step.join(cmd_part)
        try:
            value_vector.extend(target_vector) # 合并2个列表剩余的部分
            self.cursor.execute(cmd_update_line, value_vector) # 同样采用占位符的方式来防止sql注入
            print('UPDATE LINE SINGLE SUCCESS.')
        except:
            print('UPDATE LINE SINGLE FAILED.')

    def delete_line_targetly(self, table_name, target_vector):
        # 根据目标删除某一行的数据
        cmd_part = ['DELETE']
        cmd_part.append('FROM')
        cmd_part.append(str(table_name))
        cmd_part.append('WHERE')
        cmd_part.append(str(target_vector.pop(0)))
        cmd_part.append('=')
        cmd_part.append('?')
        step = ' '
        cmd_delete_line = step.join(cmd_part)
        try:
            self.cursor.execute(cmd_delete_line, target_vector)
            print('DELETE LINE SUCCESS.')
        except:
            print('DELETE LINE FAILED.')
        
    def search_line_all(self, table_name):
        # 搜索全表，往后会改成搜索前N项，点击下一页后再搜索N项，以此类推
        cmd_part = ['SELECT']
        cmd_part.append('*')
        cmd_part.append('FROM')
        cmd_part.append(str(table_name))
        step = ' '
        cmd_search_line_all = step.join(cmd_part)
        try:
            self.cursor.execute(cmd_search_line_all)
            print('SEARCH LINE ALL SUCCESS.')
            return self.cursor.fetchall() # 返回结果
        except:
            print('SEARCH LINE ALL FAILED.')
        
    def search_line_targetly(self, table_name, target_vector):
        # 根据目标搜索某一行数据
        cmd_part = ['SELECT']
        cmd_part.append('*')
        cmd_part.append('FROM')
        cmd_part.append(str(table_name))
        cmd_part.append('WHERE')
        cmd_part.append(str(target_vector.pop(0)))
        cmd_part.append('=')
        cmd_part.append('?')
        step = ' '
        cmd_search_line_targetly = step.join(cmd_part)
        print(cmd_search_line_targetly)
        try:
            self.cursor.execute(cmd_search_line_targetly, target_vector)
            print('SEARCH LINE TARGETLY SUCCESS.')
            return self.cursor.fetchall()
        except:
            print('SEARCH LINE TARGETLY FAILED.')
    
    def search_full_text(self, table_name, column_list, key_word):
        # 根据关键字和目标列进行全文搜索
        # SELECT * FROM table_name WHERE column_list MATCH 'software'
        cmd_part = ['SELECT']
        cmd_part.append('*')
        cmd_part.append('FROM')
        cmd_part.append(str(table_name))
        cmd_part.append('WHERE')
        cmd_part.append(str(column_list.pop(0)))
        cmd_part.append('LIKE')
        cmd_part.append('\'%' + str(key_word) + '%\'')
        step = ' '
        cmd_search_full_text = step.join(cmd_part)
        try:
            self.cursor.execute(cmd_search_full_text)
            print('SEARCH FULL TEXT SUCCESS.')
            return self.cursor.fetchall()
        except:
            print('SEARCH FULL TEXT FAILED.')