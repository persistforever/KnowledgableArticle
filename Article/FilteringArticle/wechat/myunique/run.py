# -*- encoding = gb18030 -*-

# package importing start
import sys

from myunique.unique import Unique
from basic.word import Word
from file.file_operator import TextFileOperator
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, source_path, title_path, unique_path) :
        source_list = self.read_source_article(source_path)
        title_list = self.read_participle_title(title_path)
        article_dict = self.constr_article_dict(source_list, title_list)
        unique_tool = Unique()
        unique_dict = unique_tool.unique(article_dict)
        unique_list = self.constr_article_list(unique_dict)
        self.write_unique_list(unique_list, unique_path)

    def read_source_article(self, source_path) :
        """ Read source article.
            Each row is an article.
            Colunm[0] is the id of article.
            Column[1:] is the attributes of article.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(source_path)
        entry_list = data_list[0]
        source_list = []
        for data in data_list[1:] :
            if len(data) >= len(entry_list) :
                article = dict()
                article['id'] = data[0]
                article['url'] = data[1]
                article['pub_time'] = data[2]
                article['title'] = data[3]
                article['content'] = data[4]
                article['n_zan'] = data[5]
                article['n_forward'] = data[6]
                article['n_click'] = data[7]
                article['n_collect'] = data[8]
                article['read_time'] = data[9]
                article['finish_rate'] = data[10]
                source_list.append(article)
        return source_list

    def read_participle_title(self, title_path) :
        """ Read participle title.
            Each row is an article.
            Colunm[0] is the id of article.
            Column[1:] is the word of participle title.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(title_path)
        entry_list = data_list[0]
        source_list = list()
        for data in data_list[1:] :
            if len(data) >= len(entry_list) :
                article = dict()
                article['id'] = data[0]
                article['participle_title'] = [Word(word) for word in data[1].split(' ')]
                source_list.append(article)
        return source_list

    def constr_article_dict(self, source_list, title_list) :
        """ Construct article dict.
            Key is id of article.
            Value is an article dict.
        """
        article_dict = dict()
        for article in source_list :
            key = article['id']
            if key not in article_dict :
                article_dict[key] = dict()
            for attr in article :
                article_dict[key][attr] = article[attr]
        for article in title_list :
            key = article['id']
            if key in article_dict :
                for attr in article :
                    article_dict[key][attr] = article[attr]
        return article_dict

    def constr_article_list(self, unique_dict) :
        """ Construct article list.
            Each element is an article list.
        """
        article_list = list()
        for id in unique_dict :
            article = list()
            article.append(unique_dict[id]['id'])
            article.append(unique_dict[id]['url'])
            article.append(unique_dict[id]['pub_time'])
            article.append(unique_dict[id]['title'])
            article.append(unique_dict[id]['content'])
            article.append(unique_dict[id]['n_zan'])
            article.append(unique_dict[id]['n_forward'])
            article.append(unique_dict[id]['n_click'])
            article.append(unique_dict[id]['n_collect'])
            article.append(unique_dict[id]['read_time'])
            article.append(unique_dict[id]['finish_rate'])
            article_list.append(article)
        return article_list

    def write_unique_list(self, unique_list, unique_path) :
        """ Write unique article list.
            Each row is an article.
            Colunm[0] is the id of article.
            Column[1:] is the attributes of article.
        """
        file_operator = TextFileOperator()
        entry_list = ['id', 'url', 'pub_time', 'title', 'content', \
            'n_zan', 'n_forward', 'n_click', 'n_collect', 'read_time', 'finish_rate']
        data_list = list()
        data_list.append(entry_list)
        for article in unique_list :
            data_list.append(article)
        file_operator.writing(data_list, unique_path)