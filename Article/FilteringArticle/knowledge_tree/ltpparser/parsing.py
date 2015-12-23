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
# package importing end


class SentenceParsing :

    def __init__(self) :
        self.removed_pos = [u'q', u'r', u'v', u'a', u'nh', u'z', u'nd', u'm']
        pass

    def read_sentence(self, sentence_path) :
        """ Read sentence. """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(sentence_path)
        return data_list

    def read_parsed(self, parse_path) :
        """ Read parsed sentence. """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(parse_path)
        sentence_list = list()
        for idx, data in enumerate(data_list) :
            word_list = json.loads(data[0])
            good = False
            for word in word_list :
                if word[u'relate'] == u'HED' and word['cont'] == u'\u53d1\u578b' :
                    good = True
            if good :
                for word in word_list :
                    if word[u'relate'] == u'ATT' :
                        worda = word[u'cont'] + u'<:>' + word[u'pos']
                        wordb = word_list[word[u'parent']][u'cont'] + u'<:>' + \
                            word_list[word[u'parent']][u'pos']
                        sentence_list.append([worda, wordb])
        return sentence_list

    def read_word(self, parse_path) :
        """ Read parsed sentence. """
        titles = self.read_parsed1(parse_path)
        file_operator = TextFileOperator()
        data_list = file_operator.reading(parse_path)
        word_dict = dict()
        sentences = []
        for idx in titles.values() :
            data = data_list[idx]
            sentences.append(json.loads(data[0]))
        for word_list in sentences :
            hair_idx = -1
            for idx, word in enumerate(word_list) :
                if word['cont'] == u'\u53d1\u578b' :
                    hair_idx = idx 
            if hair_idx != -1 :
                for idx, word in enumerate(word_list) :
                    if word['parent'] == hair_idx and word['relate'] == u'ATT' and \
                        word[u'pos'] not in self.removed_pos : #and (hair_idx-idx) <= 2 :
                        if word[u'pos'] == u'nt' :
                            word_string = word[u'cont'] + u'<:>' + u't'
                        else :
                            word_string = word[u'cont'] + u'<:>' + word[u'pos']
                        if word_string not in word_dict :
                            word_dict[word_string] = 0
                        word_dict[word_string] += 1
        word_sort = sorted(word_dict.iteritems(), key=lambda x:x[1], reverse=True)
        return [word[0] for word in word_sort if word[1] >= 3]

    def read_parsed1(self, parse_path) :
        """ Read parsed sentence. """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(parse_path)
        titles = dict()
        for idx, data in enumerate(data_list) :
            word_list = json.loads(data[0])
            good = False
            for word in word_list :
                if word[u'relate'] == u'HED' and word['cont'] == u'\u53d1\u578b' :
                    good = True
            if good :
                name = ''.join(sorted([word[u'cont'] for word in word_list \
                    if word[u'pos'] not in self.removed_pos]))
                if name not in titles :
                    titles[name] = idx
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