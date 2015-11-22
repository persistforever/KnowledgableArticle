# -*- encoding = gb18030 -*-
""" supervised classifier 
    1. MultiConditionClassifier 
"""
import numpy as np
from base import BaseClassifier
from sklearn import svm


class SvmClassifier(BaseClassifier) :
    
    def sorting(self, train_dataset, train_label, article_list) :
        clf = svm.LinearSVC(penalty='l2', C=10)
        clf.fit(train_dataset, train_label)
        print 'training classifier finished ...'
        for article in article_list :
            score_set = clf.decision_function(np.array(article.feature_set).reshape(1, -1))
            article.score = score_set[0]
        sorted_article_list = sorted(article_list, key=lambda article: article.score, reverse=True)
        return sorted_article_list