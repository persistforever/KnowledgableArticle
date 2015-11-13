# -*- encoding = utf8 -*-
'''
Feature Selector :
    1. chique selector
    2. entropy selector
    3. correlation coefficient selector
'''
import codecs
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, cross_validation
from sklearn.cross_validation import KFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import chi2
from sklearn.tree import DecisionTreeClassifier


class CorrcoefSelector :
    # attributes
    similarity = None
    threshold = 0.0
    selectedset = []

    # methods
    def __init__(self, threshold=0.85) :
        self.threshold = threshold

    def constrSimilarity(self, dataset) :
        self.similarity = np.corrcoef(dataset, rowvar=0)
        return self.similarity

    def selecting(self, dataset) :
        self.constrSimilarity(dataset)
        simset = []
        for i in range(len(self.similarity)) :
            for j in range(i+1, len(self.similarity)) :
                if self.similarity[i, j] >= self.threshold :
                    simset.append([i, j])
        simcluster = []
        for i, j in simset :
            finded = False
            for cluster in simcluster :
                if i in cluster :
                    cluster[j] = None
                    finded = True
                elif j in cluster :
                    cluster[i] = None
                    finded = True
            if not finded :
                cluster = dict()
                cluster[i] = None
                cluster[j] = None
                simcluster.append(cluster)
        # print simcluster
        self.selectedset = []
        for idx in range(len(dataset[0])) :
            needadd = True
            for cluster in simcluster :
                if idx in cluster :
                    needadd = False
                    break
            if needadd :
                self.selectedset.append(idx)
        for cluster in simcluster :
            self.selectedset.append(cluster.keys()[0])
        return self.featureTransform(dataset)

    def featureTransform(self, dataset) :
        selecteddataset = np.zeros(shape=(dataset.shape[0], 1))
        for idx in range(dataset.shape[1]) :
            if idx in self.selectedset :
                selecteddataset = np.column_stack((selecteddataset, dataset[:, idx]))
        return np.array(selecteddataset)[:, 1:selecteddataset.shape[1]]
                    

class ChisquaredSelector :
    # attributes
    threshold = 0.0

    # methods
    def __init__(self, threshold=0.1) :
        self.threshold = threshold

    def selecting(self, dataset, label) :
        featurescore, pvalue = chi2(dataset, label)
        selectedset = []
        for idx in range(len(featurescore)) :
            if featurescore[idx] >= self.threshold :
                selectedset.append(idx)
        selecteddataset = np.zeros(shape=(dataset.shape[0], 1))
        for idx in range(dataset.shape[1]) :
            if idx in selectedset :
                selecteddataset = np.column_stack((selecteddataset, dataset[:, idx]))
        return np.array(selecteddataset)[:, 1:selecteddataset.shape[1]]                   


class InfomationGainSelector :
    # attributes
    threshold = 0.0

    # methods
    def __init__(self, threshold=0.1) :
        self.threshold = threshold

    def selecting(self, dataset, label) :
        clf = DecisionTreeClassifier(criterion='entropy')
        featurescore = clf.fit(dataset, label).feature_importances_
        selectedset = []
        for idx in range(len(featurescore)) :
            if featurescore[idx] >= self.threshold :
                selectedset.append(idx)
        selecteddataset = np.zeros(shape=(dataset.shape[0], 1))
        for idx in range(dataset.shape[1]) :
            if idx in selectedset :
                selecteddataset = np.column_stack((selecteddataset, dataset[:, idx]))
        return np.array(selecteddataset)[:, 1:selecteddataset.shape[1]]