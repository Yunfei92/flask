from datetime import datetime

from sql import SQL
from modelsAdmin import Admin

time_format = '%Y-%m-%d %H:%M:%S'
id_fomat = '%Y%m%d%H%M%S'

class Article(object):


    def __init__(self):
        self.table_name = 'articles'
        self.sql = SQL()
        self.tags = [
            ('NOTICE','通知'),
            ('SHOW','展示'),
            ('EXP','经验'),
            ('LOG','日志')
        ]
        self.flags = [
            ('ONLINE','在线发布文档'),
            ('OFFLINE','离线发布文档'),
            ('SYSTEM','系统文档'),
            ('BACKUP','备份文档')
        ]
        self.id = None
        self.title = None
        self.author = None
        self.tag = None
        self.flag = None
        self.create_time = None
        self.update_time = None
        self.txt_markdown = None
        self.txt_html = None
        self.reading_times = None
        self.admin_id = None

    def get_sql(self):
        return self.sql
    
    def get_table_name(self):
        return self.table_name

    def get_title(self):
        return self.title

    def get_tag_name(self):
        return self.tag
    
    def get_flag_name(self):
        return self.flag

    def verify_tag_is_NOTICE(self):
        return self.tag == 'NOTICE'

    def verify_flag_is_ONLINE(self):
        return self.flag == 'ONLINE'

    def get_create_time(self):
        return self.create_time

    def get_update_time(self):
        return self.update_time

    def get_datetime(self):
        now_time = datetime.now()
        return now_time

    def get_admin_info(self):
        print('1')
        admin = Admin()
        admin.get_admin_object(self.admin_id)
        print(admin.account)
        return admin

    def set_id(self):
        if self.id is None:
            create_time_object = datetime.strptime(self.create_time, time_format)
            self.id = create_time_object.strftime(id_fomat)

    def form_to_object(self, form):
        # 从form中获取数据，保存到对象中去
        if self.create_time is None:
            self.create_time = self.get_datetime().strftime(time_format)
        self.update_time = self.get_datetime().strftime(time_format)
        print(self.create_time)
        self.set_id()
        self.reading_times = 0 # 以后再做阅读次数的功能

        self.title = form.title.data
        self.author = form.author.data
        self.tag = form.tag.data
        self.flag = form.flag.data
        self.txt_markdown = form.txt_markdown.data
        self.txt_html = form.txt_markdown.data

    def new_article(self, admin_id):
        value_list = [self.id]
        value_list.append(self.title)
        value_list.append(self.author)
        value_list.append(self.tag)
        value_list.append(self.flag)
        value_list.append(self.create_time)
        value_list.append(self.update_time)
        value_list.append(self.txt_markdown)
        value_list.append(self.txt_html)
        value_list.append(self.reading_times)
        value_list.append(admin_id)
        self.sql.add_line(self.table_name, value_list)

    def update_article(self):
        value_list = [self.title]
        value_list.append(self.author)
        value_list.append(self.tag)
        value_list.append(self.flag)
        value_list.append(self.update_time)
        value_list.append(self.txt_markdown)
        value_list.append(self.txt_html)
        value_list.append(self.reading_times)
        column_list = ['title', 'author', 'tag', 'flag', 'update_time', 'txt_markdown', 'txt_html', 'reading_times']
        target_vector = ['id', self.id]
        self.sql.update_line_part(self.table_name, column_list, value_list, target_vector)

    def delete_article(self):
        target_vector = ['id', self.id]
        if self.flag == 'BACKUP':
            self.sql.delete_line_targetly(self.table_name, target_vector)
            return 'CLEAR DELETE.'
        else:
            value_vector = ['flag', 'BACKUP']
            self.sql.update_line_single(self.table_name, value_vector, target_vector)
            return 'BACKUP DELECT.'

    def result_to_object(self, sql_result):
        # sql_result：一行数据是一个元组，整个数据是一个列表；[(-),...]
        # 从sql_result中获取数据，保存到对象中去
        if sql_result != []:
            result_tuple = sql_result[0]
            self.id = result_tuple[0]
            self.title = result_tuple[1]
            self.author = result_tuple[2]
            self.tag = result_tuple[3]
            self.flag = result_tuple[4]
            self.create_time = result_tuple[5]
            self.update_time = result_tuple[6]
            self.txt_markdown = result_tuple[7]
            self.txt_html = result_tuple[8]
            self.reading_times = result_tuple[9]
            self.admin_id = result_tuple[10]
        else:
            self = None

    def result_to_object_list(self, sql_result):
        # 从sql_result中获取数据，保存为对象列表
        article_list = []
        if sql_result != []:
            for i in range(len(sql_result)):
                article = Article()
                article.result_to_object([sql_result.pop()])
                article_list.append(article)
        return article_list

    def search_by_id(self, id):
        # 根据文章id搜索数据库，返回本article对象
        target_vector = ['id', id]
        result = self.sql.search_line_targetly(self.table_name, target_vector)
        self.result_to_object(result)
    
    def search_by_tag(self, tag):
        # 根据文章tag搜索数据库，返回一个object_list
        target_vector = ['tag', tag]
        sql_result = self.sql.search_line_targetly(self.table_name, target_vector)
        return self.result_to_object_list(sql_result)

    def search_by_admin_id(self, admin_id):
        # 根据admin_id搜索数据库
        target_vector = ['admin_id', admin_id]
        print('11111111111111')
        print(admin_id)
        sql_result = self.sql.search_line_targetly(self.table_name, target_vector)
        print(sql_result)
        return self.result_to_object_list(sql_result)
    
    def search_by_key_word(self, key_word):
        # 根据关键字进行全文搜索，以后再做的功能
        column_list = ['txt_html'] # 目前仅支持在此列内进行全文搜索
        sql_result = self.sql.search_full_text(self.table_name, column_list, key_word )
        return self.result_to_object_list(sql_result)

    def search_all(self):
        # 搜索全部文章，返回一个object_list
        sql_result = self.sql.search_line_all(self.table_name)
        return self.result_to_object_list(sql_result)
    
    def set_spea(self, spea_name):
        # 设置文档为4种特殊文档
        table_name = 'indexs'
        value_vector = ['article_id', self.id]
        target_vector = ['name', spea_name]
        self.sql.update_line_single(table_name, value_vector, target_vector)

    def get_spea_name(self):
        # 获得spea_name，如果不是spea，则返回None
        table_name = 'indexs'
        sql_result = self.sql.search_line_all(table_name)
        result = []
        for i in range(len(sql_result)):
            if self.id in sql_result[i]:
                result.append(sql_result[i][1])
        if len(result) == 0:
            return '' # 此处不能返回None，需要返回一个空字符串
        else:
            return result # 此处返回一个spea_name的列表，防止多个spea设置情况的出现


