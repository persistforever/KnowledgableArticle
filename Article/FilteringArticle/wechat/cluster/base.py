# -*- encoding = gb18030 -*-

# package importing start
import codecs
import numpy as np

import gensim
from sklearn import metrics

from basic.article import Article
from basic.word import Word
from file.path_manager import PathManager
from file.file_operator import TextFileOperator
from qa.word_cluster import WordCluster
from sklearn.cluster import KMeans, SpectralClustering
from sklearn import metrics
# package importing end


class BaseCluster :

    def __init__(self, corpus_path='', tfidf_path='', dict_path='', w2v_path='', lda_path='') :
        self.mmcorpus, self.tfidf_model, self.dictionary, self.word2vec, self.lda_model = \
            self._read_model(corpus_path, tfidf_path, dict_path, w2v_path, lda_path)

    def _read_model(self, corpus_path, tfidf_path, dict_path, w2v_path, lda_path) :
        """ Read models. """
        mmcorpus = gensim.corpora.MmCorpus(corpus_path)
        tfidf_model = gensim.models.TfidfModel.load(tfidf_path)
        dictionary = gensim.corpora.Dictionary.load(dict_path)
        word2vec = None # gensim.models.Word2Vec.load(w2v_path)
        lda_model = gensim.models.LdaModel.load(lda_path)
        return mmcorpus, tfidf_model, dictionary, word2vec, lda_model

    def read_test_label(self, data_path) :
        """ Read test label of cluster. """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(data_path)
        self._article_label_dict = dict()
        for data in data_list[1:] :
            if data[0] not in self._article_label_dict :
                self._article_label_dict[data[0]] = int(data[4])

    def write_article_topic(self, doc_topic_, label_path='') :
        """ Write article topic. 
            Each row of the file is a article.
            column[0] of the file is id.
            column[1] of the file is label.
        """
        data_list = []
        for idx, tuple_list in enumerate(doc_topic_) :
            data = []
            if idx == 0 :
                for key, value in tuple_list :
                    data.append(key)
            else :
                for key, value in tuple_list :
                    data.append(value)
            data_list.append(data)
        file_operator = TextFileOperator()
        file_operator.writing(data_list, label_path)