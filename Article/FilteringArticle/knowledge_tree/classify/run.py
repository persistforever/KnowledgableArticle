# -*- encoding = gb18030 -*-

# package importing start
import sys
import numpy as np

# import gensim

from basic.word import Word
from file.file_operator import TextFileOperator
from basic.market import PickleMarket, JsonMarket
import classify.selector as selector
from classify.classifier import SvmClassifier
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, article_path, article_market_path, \
            pos_path, punc_path, klword_path, feature_path, feature_market_path, \
            train_path, test_path) :
        """ function for script to drive. """
        # self.run_convert_article(article_path, article_market_path)
        # self.run_feature_select(article_market_path, pos_path, punc_path, klword_path, \
        #                        feature_path, feature_market_path)
        self.run_classify(train_path, test_path)

    def run_convert_article(self,  article_path, article_market_path) :
        articles = self.read_article(article_path)
        # articles = self.read_participle(articles, participle_path)
        loader = PickleMarket()
        loader.dump_market(articles, article_market_path)
        print 'finish.'

    def run_feature_select(self, article_market_path, pos_path, punc_path, klword_path, \
        feature_path, feature_market_path) :
        loader = PickleMarket()
        pos_selector = selector.PosExtractor(pos_path, w=10)
        token_selector = selector.TokenExtractor(punc_path)
        word_selector = selector.WordExtractor(klword_path)
        articles = loader.load_market(article_market_path)
        length = len(articles) - 1
        for idx, article in enumerate(articles) :
            article['features'] = list()
            article['features'].extend(pos_selector.extract_feature(article['participle_content']))
            article['features'].extend(token_selector.extract_feature(article['title'], article['content'], \
                                                                      article['participle_title'], \
                                                                      article['participle_content']))
            article['features'].extend(word_selector.extract_feature(article['participle_title'], \
                                                                      article['participle_content']))
            print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        featuresets = [[article['id']] + article['features'] + [article['label']] for article in articles]
        file_operator = TextFileOperator()
        file_operator.writing(featuresets, feature_path)
        loader.dump_market(featuresets, feature_market_path)
        print 'finish'

    def run_classify(self, train_path, test_path) :
        loader = PickleMarket()
        articles = loader.load_market(train_path)
        train_dataset = np.array([np.array(article[1:-1]) for article in articles])
        train_label = np.array([np.array(int(article[-1])) for article in articles])
        articles = loader.load_market(test_path)
        test_dataset = np.array([np.array(article[1:-1]) for article in articles])
        test_label = np.array([np.array(int(article[-1])) for article in articles])
        # for c in range(1, 10000, 100) :
        classifier = SvmClassifier()
        train_dataset = classifier.normalize(train_dataset)
        test_dataset = classifier.normalize(test_dataset)
        classifier.training(train_dataset, train_label)
        test_class = classifier.testing(test_dataset)
        print 'performance is %.8f' % (classifier.evaluation(test_label, test_class))
        print 'finish'

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
                article['title'] = data[2]
                article['content'] = data[3]
                article['participle_title'] = [Word(word) for word in data[4].split(' ')]
                article['participle_content'] = [Word(word) for word in data[5].split(' ')]
                article['label'] = data[6]
                source_list.append(article)
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return source_list

    def read_participle(self, articles, participle_path) :
        """ Read participle title.
            Each row is an article.
            Colunm[0] is the id of article.
            Column[1] is the word of participle title.
            Column[2] is the word of participle content.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(participle_path)
        entry_list = data_list[0]
        article_dict = dict()
        length = len(data_list[1:]) - 1
        for idx, data in enumerate(data_list[1:]) :
            if len(data) >= len(entry_list) :
                article = dict()
                article['id'] = data[0]
                article['participle_title'] = [Word(word) for word in data[1].split(' ')]
                article['participle_content'] = [Word(word) for word in data[2].split(' ')]
                article_dict[article['id']] = article
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        length = len(articles) - 1
        for idx, article in enumerate(articles) :
            if article['id'] in article_dict :
                article['participle_title'] = article_dict[article['id']]['participle_title']
                article['participle_content'] = article_dict[article['id']]['participle_content']
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return articles