# -*- encoding = gb18030 -*-

# package importing start
import sys

# import gensim

from basic.word import Word
from file.file_operator import TextFileOperator
from pretreate.advertice import RemoveAdvertice
from pretreate.unique import Unique
from pretreate.segementor import ContentSegementor
from pretreate.simplifier import ContentSimplifier
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, article_path, participle_title_path, treated_article_path) :
        """ function for script to drive. """
        self.run_pretreate(article_path, participle_title_path, treated_article_path)

    def run_pretreate(self,  article_path, participle_title_path, treated_article_path) :
        articles = self.read_article(article_path)
        titles = self.read_participle_title(participle_title_path)
        # remove advertices
        processor = RemoveAdvertice()
        indexs_adv = [articles[index]['id'] for index in processor.remove_advertice( \
            [article['title'] for article in articles])]
        print 'remove advertices finished ...'

        # remove duplications
        processor = Unique()
        indexs_unique = [titles[index]['id'] for index in processor.unique( \
            [article['participle_title'] for article in titles])]
        indexs_dict = dict().fromkeys(set(indexs_adv) & set(indexs_unique))
        remained_articles = [article for article in articles if article['id'] in indexs_dict]
        print 'remove duplications finished ...'

        # remove redundances
        segmentor = ContentSegementor()
        simplifier = ContentSimplifier()
        unredundant_articles = self.remove_redundance(remained_articles, segmentor, simplifier)
        print 'remove redundances finished ...'

        # remove short texts
        treated_articles = [article for article in unredundant_articles if len(article['content']) >= 300]
        print 'remove short texts finished ...'

        self.write_article(treated_articles, treated_article_path)
        print 'finish'

    def remove_redundance(self, article_list, segmentor, simplifier) :
        """ Segment title and content of article. """
        length = len(article_list) - 1
        for idx, article in enumerate(article_list) :
            segmented_content = segmentor.segement(article['content'])
            tag_content = [simplifier.tag_sentence(sentence) for sentence in segmented_content]
            tag_content = simplifier.filter_tail(tag_content)
            tag_content = simplifier.filter_head(tag_content)
            article['segmented_content'] = [content[0] for content in tag_content]
            article['content'] = u'\u3000'.join(article['segmented_content'])
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return article_list

    def read_article(self, article_path) :
        """ Read source article.
            Each row is an article.
            Colunm[0] is the id of article.
            Column[1:] is the attributes of article.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(article_path)
        entry_list = data_list[0]
        source_list = []
        length = len(data_list[1:]) - 1
        for idx, data in enumerate(data_list[1:]) :
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
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
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
        length = len(data_list[1:]) - 1
        for idx, data in enumerate(data_list[1:]) :
            if len(data) >= len(entry_list) :
                article = dict()
                article['id'] = data[0]
                article['participle_title'] = [Word(word) for word in data[1].split(' ')]
                source_list.append(article)
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return source_list

    def write_article(self, articles, article_path) :
        """ Write source article.
            Each row is an article.
            Colunm[0] is the id of article.
            Column[1:] is the attributes of article.
        """
        data_list = list()
        entry_list = ['id', 'url', 'title', 'content']
        data_list.append(entry_list)
        length = len(articles) - 1
        for idx, article in enumerate(articles) :
            data = [article['id'], article['url'], article['title'], article['content']]
            data_list.append(data)
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        file_operator = TextFileOperator()
        file_operator.writing(data_list, article_path)