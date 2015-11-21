# -*- encoding = gb18030 -*-
'''
Basic module
    Corpus class
'''
from basic.article import Article
from file.file_operator import CSVFileOperator, TextFileOperator
from file.path_manager import PathManager


class Corpus :

    def __init__(self) :
        pass

    def read_article_list(self, file_name) :
        """ Read article list from file_name.
        Each row of the file is a article.
        Each column of the file is the attributes of article. """
        data_list = TextFileOperator.reading(PathManager.get_output_article())
        for data in data_list :
            article = Article()
            if len(data) >= 4 :
                article.import_article(data)