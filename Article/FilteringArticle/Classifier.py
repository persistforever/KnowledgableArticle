# -*- encoding = utf8 -*-
'''
Classifier :
    1. multi-condition sorting classifier
    2. SVM classifier
    3. feature selected SVM classifier
'''
import codecs 
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, cross_validation
from sklearn.cross_validation import KFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import FeatureSelector


class MulticonditionSortingClassifier :
    # attributes

    # ---------- init -----------
    def __init__(self) :
        pass

    # ---------- training and test ----------
    def processing(self, artlist) :
        sortedlist = sorted(artlist, key=lambda x: ( \
            x.featureset[21], x.featureset[23], x.featureset[25], x.featureset[27], \
            -x.featureset[15], -x.featureset[13], -x.featureset[1]), reverse=True)
        return sortedlist


class SVMClassifier :
    # ----- attributes -----

    # ---------- init -----------
    def __init__(self) :
        pass

    # ---------- training and test ----------
    def processing(self, traindataset, trainlabel, artlist) :
        clf = svm.SVC(kernel='linear', probability=True)
        clf.fit(traindataset, trainlabel)
        print 'training classifier finished ...'
        for article in artlist :
            article.testlabel = clf.predict_proba(np.array(article.featureset[0:]).reshape(1, -1))
            article.testlabel = article.testlabel[0][1]
        sortedlist = sorted(artlist, key=lambda x: x.testlabel, reverse=True)
        return sortedlist


class FeatureSelectedSVMClassifier :
    # attributes

    # ---------- init -----------
    def __init__(self) :
        pass

    # ---------- training and test ----------
    def processing(self, traindataset, trainlabel, artlist) :
        clf = svm.SVC(kernel='linear', probability=True)
        selector = FeatureSelector.CorrcoefSelector(threshold=0.95)
        clf.fit(selector.selecting(traindataset), trainlabel)
        print 'training classifier finished ...'
        for article in artlist :
            article.testlabel = clf.predict_proba(selector.featureTransform(np.array([article.featureset])))
            article.testlabel = article.testlabel[0][1]
        sortedlist = sorted(artlist, key=lambda x: x.testlabel, reverse=True)
        return sortedlist


class ClassifierTester :
    # ----- attributes -----

    # ---------- process methods ----------
    def crossValidation(self, dataset, label, n_folds=4) :
        kf = KFold(len(dataset), n_folds=n_folds, shuffle=True)
        accurancy = []
        for train, test in kf :
            train_dataset, test_dataset, train_label, test_label = dataset[train], dataset[test], label[train], label[test]
            clf = svm.SVC(kernel=self.kernel, probability=True)
            clf.fit(train_dataset, train_label)
            test_class = []
            for data in test_dataset :
                test_class.append(clf.predict(np.array(data).reshape(1, -1)))
            test_class = np.array(test_class)
            accurancy.append(self.evaluation(test_class, test_label))
        return np.mean(accurancy)

    def evaluation(self, test_class, test_label) :
        acnum = 0
        for idx in range(len(test_class)) :
            if test_class[idx] == test_label[idx] :
                acnum += 1
            if len(test_class) == 0 :
                accurancy = 0.0
            else :
                accurancy = 1.0 * acnum / len(test_class)
        return accurancy

    def processing(self, dataset, label) :
        dataset = np.column_stack((dataset[:, 0:21], dataset[:, 22], dataset[:, 24], dataset[:, 26], dataset[:, 28:]))
        experiments = []
        for n in range(2, 6) :
            experiment = []
            # experiment.append(self.crossValidation(dataset[:, 0:12], label, n_folds=n))
            # experiment.append(self.crossValidation(dataset[:, 12:18], label, n_folds=n))
            # experiment.append(self.crossValidation(dataset[:, 28:], label, n_folds=n))
            # experiment.append(self.crossValidation(dataset[:, 0:18], label, n_folds=n))
            experiment.append(self.crossValidation(dataset[:, :], label, n_folds=n))
            selector = FeatureSelector.CorrcoefSelector(threshold=0.85)
            experiment.append(self.crossValidation(selector.selecting(dataset), label, n_folds=n))
            selector = FeatureSelector.ChisquaredSelector(threshold=0.1)
            experiment.append(self.crossValidation(selector.selecting(dataset, label), label, n_folds=n))
            selector = FeatureSelector.InfomationGainSelector(threshold=1e-3)
            experiment.append(self.crossValidation(selector.selecting(dataset, label), label, n_folds=n))
            print experiment
            experiments.append(experiment)
        color = ['yo--', 'ro--', 'go--', 'bo--', 'mo--']
        lgd = ('no', 'corrcoef', 'chisquared', 'infomationgain', 'token+info+pos')
        p = []
        for idx in range(len(experiments[0])) :
            p.append(plt.plot(range(2, 6), [t[idx] for t in experiments], color[idx]))
        plt.title('different model evaluation')
        plt.xlabel('# folds of cross validation')
        plt.ylabel('accurancy')
        # plt.axis([1, 11, 0.6, 0.8])
        plt.legend(tuple([t[0] for t in p]), lgd[0: len(experiments[0])])
        plt.show()

    def plotDistribution(self, dataset, col) :
        plt.hist(dataset[:, col], bins=20)
        plt.title('distribution')
        plt.xlabel('value')
        plt.ylabel('frequence')
        plt.show()