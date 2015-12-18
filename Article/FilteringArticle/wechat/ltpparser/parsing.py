# -*- encoding = gb18030 -*-

# package importing start
import numpy as np
import math
import json

from sklearn.cluster import KMeans
from sklearn import metrics
import gensim

from file.path_manager import PathManager
from file.file_operator import TextFileOperator
from basic.word import Word
from cluster.base import BaseCluster
# package importing end


class SentenceParsing :

    def __init__(self) :
        pass

    def read_sentence(self, sentence_path) :
        """ Read sentence. """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(sentence_path)
        return data_list

    def read_parsed2(self, parse_path) :
        """ Read parsed sentence. """
        remain_pos = [u'n', u'nt', u'b', u'ns']
        file_operator = TextFileOperator()
        data_list = file_operator.reading(parse_path)
        sentence_dict = dict()
        for idx, data in enumerate(data_list) :
            word_list = json.loads(data[0])
            good = False
            for word in word_list :
                if word[u'relate'] == u'HED' and word['cont'] == u'\u53d1\u578b' :
                    good = True
            if good :
                for word in word_list :
                    if word[u'relate'] == u'ATT' :
                        if word[u'pos'] in remain_pos and word_list[word[u'parent']][u'pos'] in remain_pos :
                            worda = word[u'cont'] + u'<:>' + word[u'pos']
                            wordb = word_list[word[u'parent']][u'cont'] + u'<:>' + \
                                word_list[word[u'parent']][u'pos']
                            if worda + wordb not in sentence_dict :
                                sentence_dict[worda + wordb] = [worda, wordb]
        return sentence_dict.values()

    def read_parsed(self, parse_path) :
        """ Read parsed sentence. """
        remain_pos = [u'n', u'nt', u'b', u'ns']
        titles = self.read_parsed1(parse_path)
        file_operator = TextFileOperator()
        data_list = file_operator.reading(parse_path)
        word_dict = dict()
        for idx in titles :
            data = data_list[idx]
            word_list = json.loads(data[0])
            hair_idx = -1
            for idx, word in enumerate(word_list) :
                if word['cont'] == u'\u53d1\u578b' :
                    hair_idx = idx 
            if hair_idx != -1 :
                for idx, word in enumerate(word_list) :
                    if word['parent'] == hair_idx and word['relate'] == u'ATT' :
                        if word[u'pos'] in remain_pos :
                            word_string = word[u'cont'] + u'<:>' + word[u'pos']
                            if word_string not in word_dict :
                                word_dict[word_string] = 0
                            word_dict[word_string] += 1
        word_sort = sorted(word_dict.iteritems(), key=lambda x:x[1], reverse=True)
        return [word[0] for word in word_sort[0:100]]

    def read_parsed1(self, parse_path) :
        """ Read parsed sentence. """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(parse_path)
        titles = []
        for idx, data in enumerate(data_list) :
            word_list = json.loads(data[0])
            good = False
            for word in word_list :
                if word[u'relate'] == u'HED' and word['cont'] == u'\u53d1\u578b' :
                    good = True
            if good :
                titles.append(idx)
        return titles

    def parsing(self, sentence_list, parser) :
        """ Use parser to parsing sentence. """
        for sentence in sentence_list :
            content = parser.parsing(sentence[0])

    def word_clustering(self, word2vec, word_set, cluster) :
        word_dict = dict()
        for word in word_set :
            if word in word2vec :
                word_dict[word] = word2vec[word]
        cluster._word_clustering(word_dict)