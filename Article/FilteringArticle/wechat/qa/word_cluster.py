# -*- encoding = gb18030 -*-
""" clustering word. """
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import numpy as np
from sklearn.cluster import KMeans
from file.path_manager import PathManager
from gensim import models


class WordCluster :

    def __init__(self, word_dict, n_cluster=5) :
        self.n_cluster = n_cluster
        self.word_list = []
        for word in word_dict :
            self.word_list.append([word, word_dict[word], 0])
        self.path_manager = PathManager()
        self.word_model = models.Word2Vec.load(self.path_manager.get_tools_vector())
        self.label_list = []

    def get_label_list(self) :
        word_set = []
        index_list = []
        for idx, word in enumerate(self.word_list) :
            try :
                word_set.append(self.word_model[word[0].encode('utf8')])
                index_list.append(idx)
            except Exception, e :
                pass
        word_set = np.array(word_set)
        cls = KMeans(n_clusters=self.n_cluster, max_iter=300).fit(word_set)
        '''
        for center_vector in cls.cluster_centers_ :
            idx_dist = []
            for idx in range(word_set.shape[0]) :
                idx_dist.append([idx, \
                    sum([center_vector[i] * word_set[idx, i] for i in range(center_vector.shape[0])]) \
                    / (np.linalg.norm(center_vector) * np.linalg.norm(word_set[idx]))])
            print self.word_list[index_list[max(idx_dist, key=lambda x: x[1])[0]]].encode('gb18030')
        '''
        for idx in range(cls.labels_.shape[0]) :
            self.word_list[index_list[idx]][2] = cls.labels_[idx]
        self.word_list = sorted(self.word_list, key=lambda x: x[1], reverse=True)
        for seq in range(0, self.n_cluster) :
            self.label_list.append([None, []])
        for seq in range(0, self.n_cluster) :
            for word, num, label in self.word_list :
                if label == seq and self.label_list[seq][0] == None :
                    self.label_list[seq][0] = word
                    self.label_list[seq][1].append(word)
                    # print word.encode('gb18030')
                else :
                    self.label_list[label][1].append(word)
        return self.label_list