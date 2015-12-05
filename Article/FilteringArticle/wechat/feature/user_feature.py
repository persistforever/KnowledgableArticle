# -*- encoding = gb18030 -*-

# package importing start
from file.file_operator import TextFileOperator
from feature.base import BaseExtractor
# package importing end


class UserExtractor(BaseExtractor) :

    def __init__(self) :
        BaseExtractor.__init__(self)
    
    def extractFeature(self, article_list) :
        for article in article_list :
            n_zan = article.n_zan
            n_forward = article.n_forward
            n_click = article.n_click
            n_collect = article.n_collect
            read_time = article.read_time
            finish_rate = article.finish_rate
            article.set_features(n_zan=n_zan, n_forward=n_forward, n_click=n_click, \
                n_collect=n_collect, read_time=read_time, finish_rate=finish_rate)