# -*- encoding = gb18030 -*-
""" question and anster system clustering article. """

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


class LdaCluster :

    def __init__(self, corpus_path='', tfidf_path='', dict_path='', w2v_path='', lda_path='') :
        self.corpus_path = corpus_path
        self.tfidf_path = tfidf_path
        self.dict_path = dict_path
        self.w2v_path = w2v_path
        self.lda_path = lda_path
        self.mmcorpus, self.tfidf_model, self.dictionary, self.word2vec, self.lda_model = self._read_model()

    def _read_model(self) :
        """ Read tfidf models. """
        mmcorpus = gensim.corpora.MmCorpus(self.corpus_path)
        tfidf_model = gensim.models.TfidfModel.load(self.tfidf_path)
        dictionary = gensim.corpora.Dictionary.load(self.dict_path)
        word2vec = gensim.models.Word2Vec.load(self.w2v_path)
        lda_model = gensim.models.LdaModel.load(self.lda_path)
        return mmcorpus, tfidf_model, dictionary, word2vec, lda_model

    def read_test_label(self, data_path) :
        """ Read test label of cluster. """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(data_path)
        self._article_label_dict = dict()
        for data in data_list[1:] :
            if data[0] not in self._article_label_dict :
                self._article_label_dict[data[0]] = int(data[4])

    def read_test_class(self, article_list) :
        """ Read test class of cluster. """
        self._article_class_dict = dict().fromkeys(self._article_label_dict.keys())
        for idx, article in enumerate(article_list) :
            if article.id in self._article_class_dict :
                class_score = self.lda_model.get_document_topics(self.mmcorpus[idx], minimum_probability=0)
                self._article_class_dict[article.id] = int(max(class_score, key=lambda x: x[1])[0])

    def evaluation(self) :
        """ evaluate the accurancy of the lda model. """
        labels_true = self._article_label_dict.values()
        labels_pred = self._article_class_dict.values()
        score = metrics.adjusted_rand_score(labels_true, labels_pred)  
        print 'adjusted_rand_score is', score
        score = metrics.adjusted_mutual_info_score(labels_true, labels_pred)  
        print 'adjusted_mutual_info_score is', score
        score = metrics.homogeneity_score(labels_true, labels_pred)  
        print 'homogeneity_score is', score
        score = metrics.completeness_score(labels_true, labels_pred)  
        print 'completeness_score is', score
        adj_labels_pred = [[0, 0, 2, 1, 3][l] for l in labels_pred]
        score = 1.0 * sum([1 for idx in range(len(labels_true)) \
            if adj_labels_pred[idx] == labels_true[idx]]) / len(labels_true)
        print 'accurancy is', score