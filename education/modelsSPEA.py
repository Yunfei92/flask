from sql import SQL
from modelsArticle import Article


class SPEA(Article):
    def result_to_object(self, sql_result):
        # sql_result：一行数据是一个元组，整个数据是一个列表；[(-),...]
        # 从sql_result中获取数据，保存到对象中去
        if sql_result != []:
            result_tuple = sql_result[0]
            self.spea_id = result_tuple[0]
            self.spea_name = result_tuple[1]
            self.spea_article_id = result_tuple[2]
        else:
            self.spea_id = None
            self.spea_name = None
            self.spea_article_id = None

    def get_SPEA(self, spea_name):
        table_name = 'indexs'
        indexs_target_vector = ['name', spea_name]
        indexs_result = super().get_sql().search_line_targetly(table_name, indexs_target_vector)
        self.result_to_object(indexs_result)
        if indexs_result is not None:
            article_id = indexs_result[0][2]
            if article_id is not None:
                articles_target_vector = ['id', article_id]
                articles_result = super().get_sql().search_line_targetly(super().get_table_name(), articles_target_vector)
                if articles_result is not None:
                    super().result_to_object(articles_result)
                    print(self.get_tag_name())
                else:
                    print('[ ' + spea_name + ' ]' + ' IS NOT EXSIS.')
            else:
                print('[ ' + spea_name + ' ]' + ' IS NOT SET.')

class WebsiteInfo(SPEA):
    # 注意此处不能用__init__()方法，因为会覆盖父类方法
    def get_website_info(self):
        spea_name = 'website_info'
        super().get_SPEA(spea_name)

class UpdateInfo(SPEA):
    def get_update_info(self):
        spea_name = 'update_info'
        super().get_SPEA(spea_name)

class IndexImax(SPEA):
    def get_index_imax(self):
        spea_name = 'index_imax'
        super().get_SPEA(spea_name)
class NoticeBoard(SPEA):
    def get_notice_board(self):
        spea_name = 'notice_board'
        super().get_SPEA(spea_name)