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
from sklearn.cluster import KMeans, SpectralClustering
from cluster.base import BaseCluster
from sklearn import metrics
# package importing end


class LdaCluster(BaseCluster) :

    def __init__(self, corpus_path='', tfidf_path='', dict_path='', w2v_path='', lda_path='') :
        BaseCluster.__init__(self, corpus_path, tfidf_path, dict_path, w2v_path, lda_path)

    def read_test_class(self, article_list) :
        """ Read test class of cluster. """
        self._article_class_dict = dict().fromkeys(self._article_label_dict.keys())
        for idx, article in enumerate(article_list) :
            if article.id in self._article_class_dict :
                class_score = self.lda_model.get_document_topics(self.mmcorpus[idx], minimum_probability=0)
                self._article_class_dict[article.id] = int(max(class_score, key=lambda x: x[1])[0])

    def evaluation(self) :
        """ evaluate the accurancy of the lda model. """
        labels_true = self._article_label_dict
        labels_pred = self._article_class_dict
        '''
        score = metrics.adjusted_rand_score(labels_true, labels_pred)  
        print 'adjusted_rand_score is', score
        score = metrics.adjusted_mutual_info_score(labels_true, labels_pred)  
        print 'adjusted_mutual_info_score is', score
        score = metrics.homogeneity_score(labels_true, labels_pred)  
        print 'homogeneity_score is', score
        score = metrics.completeness_score(labels_true, labels_pred)  
        print 'completeness_score is', score
        '''
        adj_labels_pred = {id: [0, 0, 2, 1, 3][labels_pred[id]] for id in labels_pred.keys()}
        score = 1.0 * sum([1 for id in labels_true \
            if adj_labels_pred[id] == labels_true[id]] ) / len(labels_true)
        print 'accurancy is', score

    def process(self, article_list) :
        """ main process of naive bayes. """
        self.read_test_class(article_list)
        self.evaluation()