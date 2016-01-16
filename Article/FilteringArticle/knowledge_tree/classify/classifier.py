# -*- encoding = gb18030 -*-

# package importing start
import numpy as np

from sklearn import svm
from sklearn.externals import joblib
import sklearn.metrics as metrics
from sklearn import cross_validation
from sklearn import preprocessing
# package importing end


class SvmClassifier :

    def __init__(self, c=1) :
        self.c = c

    def training(self, train_dataset, train_label, cset=range(10, 1000, 10), \
        kernel='linear') :
        """ Train classifier with train_data and train_label. """
        X_train, X_test, y_train, y_test = cross_validation.train_test_split( \
            train_dataset, train_label, test_size=0.2, random_state=0)
        max_eval, max_c = 0.0, 1
        for c in cset :
            self.clf = svm.SVC(C=c, kernel=kernel, probability=True)
            self.clf.fit(X_train, y_train)
            prob_test = self.testing(X_test, type='prob')
            class_test = self.testing(X_test, type='label')
            perfor = self.evaluation(y_test, prob_test, class_test)[0]
            if perfor >= max_eval :
                max_eval = perfor
                max_c = c
        self.clf = svm.SVC(C=max_c, kernel=kernel, probability=True)
        self.clf.fit(train_dataset, train_label)
        print 'training classifier finished ...'
    
    def testing(self, test_dataset, type='prob') :
        """ Use classifier test test_data. """
        class_list = list()
        if type == 'prob' :
            for row in range(test_dataset.shape[0]) :
                class_list.append(self.clf.predict_proba(test_dataset[row, :].reshape(1, -1))[0][1])
        elif type == 'label' :
            for row in range(test_dataset.shape[0]) :
                class_list.append(self.clf.predict(test_dataset[row, :].reshape(1, -1))[0])
        return np.array(class_list)

    def normalize(self, dataset, method='mapminmax') :
        """ Normalize the dataset. """
        if method == 'mapminmax' :
            dataset = self.normalize_mapminmax(dataset)
        elif method == 'zscore' :
            dataset = self.normalize_zscore(dataset)
        return dataset

    def normalize_mapminmax(self, dataset) :
        """ Normalize the dataset using mapminmax. """
        for col in range(dataset.shape[1]) :
            maximum = max(dataset[:, col])
            minimum = min(dataset[:, col])
            for row in range(dataset.shape[0]) :
                if maximum - minimum == 0 :
                    dataset[row, col] = 0.0
                else :
                    dataset[row, col] = 1.0 * (maximum - dataset[row, col]) / (maximum - minimum)
        return dataset

    def normalize_zscore(self, dataset) :
        """ Normalize the dataset using zscore. """
        dataset = preprocessing.scale(dataset)
        return dataset

    def evaluation(self, test_label, test_prob, test_class) :
        """ Evaluate the performance. """
        '''
        posi_len = 1.0 * len([1 for idx in range(test_label.shape[0]) if test_label[idx] == 1])
        nega_len = 1.0 * len([1 for idx in range(test_label.shape[0]) if test_label[idx] == 0])
        true_posi = len([1 for idx in range(test_label.shape[0]) \
            if test_label[idx] == 1 and test_class[idx] == 1]) / posi_len
        true_nega = len([1 for idx in range(test_label.shape[0]) \
            if test_label[idx] == 0 and test_class[idx] == 0]) / nega_len
        '''
        # return metrics.f1_score(test_label, test_class, pos_label=1, average='binary')
        evl = list()
        evl.append(round(metrics.roc_auc_score(test_label, test_prob), 4))
        evl.append(round(metrics.accuracy_score(test_label, test_class), 4))
        return evl

    def storing(self, classifier, path='') :
        """ Store the classifier. """
        joblib.dump(classifier, path)
        print 'storing classifier finished ...'