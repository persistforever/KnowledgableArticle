# -*- encoding = gb18030 -*-
""" supervised classifier 
    1. MultiConditionClassifier 
"""

# package importing start
import numpy as np

from sklearn import svm
from sklearn.externals import joblib

from base import BaseClassifier
# package importing end


class SvmClassifier(BaseClassifier) :
    
    def sorting(self, test_data, article_list, clf_path='') :
        clf = joblib.load(clf_path)
        for row in range(test_data.shape[0]) :
            score_set = clf.decision_function(test_data[row, :])
            article_list[row].score = score_set[0]

    def _set_support_index(self, support_index) :
        self.support_index_list = support_index.tolist()

    def training(self, train_dataset, train_label) :
        """ Train classifier with train_data and train_label. """
        clf = svm.SVC(C=10, kernel='linear')
        clf.fit(train_dataset, train_label)
        return clf
        print 'training classifier finished ...'

    def storing(self, classifier, path='') :
        """ Store the classifier. """
        joblib.dump(classifier, path)
        print 'storing classifier finished ...'