# -*- encoding = gb18030 -*-

# package importing start
import numpy as np

from sklearn.cluster import KMeans
from sklearn import metrics
import gensim

from file.path_manager import PathManager
from file.file_operator import TextFileOperator
from basic.word import Word
# package importing end


class WordCluster :

    def __init__(self, corpus_path='', tfidf_path='', dict_path='', w2v_path='', lda_path='') :
        self.n_cluster = 3
        self.mmcorpus, self.dictionary = self._read_data(corpus_path, dict_path)

    def _read_data(self, corpus_path, dict_path) :
        """ Read gensim models. """
        mmcorpus = gensim.corpora.MmCorpus(corpus_path)
        dictionary = gensim.corpora.Dictionary.load(dict_path)
        return mmcorpus, dictionary

    def _init_model(self) :
        """ Init navie bayes model. """
        self.word_dict = dict()
        self.word_dict[self.dictionary.token2id[u'发型<:>n']] = [1.0, 0.0, 0.0]
        self.word_dict[self.dictionary.token2id[u'化妆<:>vn']] = [0.0, 1.0, 0.0]
        self.word_dict[self.dictionary.token2id[u'服饰<:>n']] = [0.0, 0.0, 1.0]
        self.prior_prob = [1.0/self.n_cluster] * self.n_cluster

    def read_test_label(self, data_path) :
        """ Read test label of cluster. """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(data_path)
        self._article_label_dict = dict()
        for data in data_list[1:] :
            if data[0] not in self._article_label_dict :
                self._article_label_dict[data[0]] = int(data[4])

    def read_test_class(self, article_list, labels_pred) :
        """ Read test class of cluster. """
        self._article_class_dict = dict().fromkeys(self._article_label_dict.keys())
        for idx, article in enumerate(article_list) :
            if article.id in self._article_class_dict :
                self._article_class_dict[article.id] = int(labels_pred[idx])

    def allocate_article(self, labels_pred) :
        """ Allocate article to clusters. 
            The same as labeling articles.
        """
        for idx, texts in enumerate(self.mmcorpus) :
            distinguished = False
            scores = [1.0] * self.n_cluster
            for label in range(self.n_cluster) :
                for word, times in texts :
                    if word in self.word_dict :
                        distinguished = True
                        scores[label] *= self.word_dict[word][label]
                scores[label] *= self.prior_prob[label]
            if distinguished :
                labels_pred[idx] = max(enumerate(scores), key=lambda x: x[1])[0]
        return labels_pred

    def update_word_dict(self, word_dict, labels_pred) :
        """ Find Discrimination words. """
        condidate_word = dict().fromkeys(self.dictionary.token2id.values(), None)
        for word in condidate_word :
            condidate_word[word] = [0.0] * self.n_cluster
        cluster_number = [0.0] * self.n_cluster
        for idx, texts in enumerate(self.mmcorpus) :
            if labels_pred[idx] != -1 :
                cluster_number[labels_pred[idx]] += 1
                for word, times in texts :
                    condidate_word[word][labels_pred[idx]] += 1
        for word in condidate_word.keys() :
            for label in range(self.n_cluster) :
                condidate_word[word][label] = 1.0 * (condidate_word[word][label] + 1) / \
                    (cluster_number[label] + len(self.dictionary))
        selected_word = self.select_condidate_word(condidate_word, threshold=0.001)
        for word in selected_word :
            self.word_dict[word] = condidate_word[word]
        return self.word_dict

    def select_condidate_word(self, condidate_word, threshold=0.01) :
        """ select score > t1 word in the condidate_word. """
        word_score = dict().fromkeys(self.dictionary.token2id.values(), None)
        for word in condidate_word.keys() :
            word_score[word] = [0.0] * self.n_cluster
            s = 1.0
            for label in range(self.n_cluster) :
                s *= condidate_word[word][label]
            for label in range(self.n_cluster) :
                if condidate_word[word][label] >= threshold :
                    score = 1.0 * ((condidate_word[word][label]) ** 2) / s
                else :
                    score = 0.0
                word_score[word][label] = score
        selected_word = []
        sorted_list = sorted(word_score.iteritems(), key=lambda x: max(x[1]), reverse=True)
        for label in range(self.n_cluster) :
            selected_label_word = []
            for word, lst in sorted_list :
                if max(lst) != 0.0 and max(enumerate(lst), key=lambda x: x[1])[0] == label:
                    selected_label_word.append(word)
            selected_word.extend(selected_label_word[0:100])
        return selected_word

    def process(self, article_list) :
        """ main process of naive bayes. """
        self._init_model()
        for step in range(0, 5) :
            labels_pred = [-1] * len(article_list)
            labels_pred = self.allocate_article(labels_pred)
            self.read_test_class(article_list, labels_pred)
            self.evaluation()
            self.word_dict = self.update_word_dict(self.word_dict, labels_pred)
        print labels_pred

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
        adj_labels_pred = [[9, 1, 2, 3][l+1] for l in labels_pred]
        score = 1.0 * sum([1 for idx in range(len(labels_true)) \
            if adj_labels_pred[idx] == labels_true[idx]]) / len(labels_true)
        print 'accurancy is', score