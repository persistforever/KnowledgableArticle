# -*- encoding = gb18030 -*-
""" question and anster system clustering article. """
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import codecs
import numpy as np
import re
import gensim
from basic.article import Article
from basic.word import Word
from file.path_manager import PathManager
from file.file_operator import TextFileOperator
from qa.word_cluster import WordCluster


class ArticleCluster :

    def __init__(self) :
        pass

    def article_clustering(self, article_list, query_list) :
        """ clustering article's keyword accordding to query. """
        while len(article_list) > 1 :
            print len(article_list)
            word_dict = self._article_tfidf(article_list, query_list)
            for article in article_list :
                print article.id.encode('gb18030'), 
                for w in article.tag_list :
                    print w.name.encode('gb18030'), 
                print
            print len([article for article in article_list if article.tag_list==[]])
            if len([article for article in article_list if article.tag_list!=[]]) <= 1 :
                break
            cls = WordCluster(word_dict, n_cluster=3)
            self.label_list = cls.get_label_list()
            outstr = 'which do you want? '
            for key, word_list in self.label_list :
                outstr += key + ' '
            outstr.strip().encode('gb18030')
            seq = int(raw_input(outstr))
            query_list.append(self.label_list[seq][0])
            perticular_article_list = []
            for article in article_list :
                for word in self.label_list[seq][1] :
                    if word in [w.name for w in article.tag_list] :
                        perticular_article_list.append(article)
                    break
            article_list = perticular_article_list
        if len(article_list) > 0 :
            print [article.id for article in article_list][0]

    def _article_tagging(self, article_list, query_list) :
        """ tagging each article. """
        word_dict = dict()
        for article in article_list :
            article.set_params(tag_list=[])
            keyword_dict = dict()
            for keyword, tfidf in article.keyword_list[0:100] :
                for query in query_list :
                    distance = self._keyword_query_distance(keyword, query, article.sub_sentence)
                    if keyword not in keyword_dict :
                        keyword_dict[keyword.name] = []
                    if distance != 0 :
                        keyword_dict[keyword.name].append(1.0 * distance * tfidf)
            for keyword in keyword_dict :
                if keyword_dict[keyword] != [] :
                    keyword_dict[keyword] = 1.0 * sum(keyword_dict[keyword]) / len(keyword_dict[keyword])
                else :
                    keyword_dict[keyword] = 0
            for word, score, in sorted(keyword_dict.iteritems(), key=lambda x: x[1], reverse=True)[0:100] :
                if score >= 3 : 
                    word_object = Word(word)
                    article.tag_list.append(word_object)
                    if word_object.name not in word_dict :
                        if word_object.name not in query_list :
                            word_dict[word_object.name] = 0
                    if word_object.name not in query_list :
                        word_dict[word_object.name] += 1
        return word_dict

    def _article_tfidf(self, article_list, query_list) :
        """ tagging each article. """
        word_dict = dict()
        for article in article_list :
            article.set_params(tag_list=[])
            for keyword, tfidf in article.keyword_list[0:5] :
                article.tag_list.append(keyword)
                if keyword.name not in word_dict :
                    if keyword.name not in query_list :
                        word_dict[keyword.name] = 0
                if keyword.name not in query_list :
                    word_dict[keyword.name] += 1
        return word_dict

    def _keyword_query_distance(self, keyword, query, sub_sentence) :
        """ calculate distance between keyword and query. """
        distance = 0.0
        for sentence in sub_sentence :
            sentence_word = [word.name for word in sentence]
            if keyword.name in sentence_word and query in sentence_word :
                # print ''.join([word.name for word in sentence])
                distance += abs(sentence_word.index(keyword.name) - \
                    sentence_word.index(query))
        if distance != 0 :
            distance = 1.0 / distance
        return distance