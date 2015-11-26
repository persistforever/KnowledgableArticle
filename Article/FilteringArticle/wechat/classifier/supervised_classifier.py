# -*- encoding = gb18030 -*-
""" supervised classifier 
    1. MultiConditionClassifier 
"""
import numpy as np
from base import BaseClassifier
from sklearn import svm


class SvmClassifier(BaseClassifier) :
    
    def sorting(self, train_dataset, train_label, article_list) :
        clf = svm.SVC(C=10, kernel='linear')
        clf.fit(train_dataset, train_label)
        self._set_support_index(clf.support_)
        print 'training classifier finished ...'
        for article in article_list :
            score_set = clf.decision_function(np.array(article.feature_set).reshape(1, -1))
            article.score = score_set[0]
        sorted_article_list = sorted(article_list, key=lambda article: article.score, reverse=True)
        return sorted_article_list

    def _set_support_index(self, support_index) :
        self.support_index_list = support_index.tolist()