from modelsArticle import Article
from modelsAdmin import Admin
from modelsSPEA import SPEA,NoticeBoard,WebsiteInfo
from sql import SQL


if __name__=='__main__':
    article = Article()
    article.search_by_id('20170510114146')
    print(article.is_spea())
    print(article.get_spea_name())