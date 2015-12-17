# -*- encoding = gb18030 -*-

# package importing start
import numpy as np
import math

from sklearn.cluster import KMeans
from sklearn import metrics
import gensim

from file.path_manager import PathManager
from file.file_operator import TextFileOperator
from basic.word import Word
from cluster.base import BaseCluster
# package importing end


class WordCluster(BaseCluster) :

    def __init__(self, corpus_path='', tfidf_path='', dict_path='', w2v_path='', lda_path='') :
        BaseCluster.__init__(self, corpus_path, tfidf_path, dict_path, w2v_path, lda_path)

    def _init_model(self) :
        """ Init navie bayes model. """
        self.word_dict = dict()
        self.seeds = []
        self.seeds.append([u'发型'])
        self.seeds.append([u'化妆', u'彩妆'])
        self.seeds.append([u'衣服', u'服饰'])
        self.n_cluster = len(self.seeds)
        '''
        self.startup_words.append([u'男'])
        self.startup_words.append([u'女'])
        '''
        self.prior_prob = [1.0/self.n_cluster] * self.n_cluster

    def read_test_class(self, article_list, labels_pred) :
        """ Read test class of cluster. """
        self._article_class_dict = dict().fromkeys(self._article_label_dict.keys())
        for idx, article in enumerate(article_list) :
            if article.id in self._article_class_dict :
                self._article_class_dict[article.id] = int(labels_pred[idx])

    def _start_up_labels(self, labels_pred, article_list) :
        """ start up to labeling article use startup words. """
        for idx, article in enumerate(article_list) :
            distinguished = False
            for label in range(self.n_cluster) :
                for word in self.seeds[label] :
                    if word in article.title :
                        distinguished = True
                        labels_pred[idx] = label
        return labels_pred

    def allocate_article(self, labels_pred) :
        """ Allocate article to clusters. 
            The same as labeling articles.
        """
        for idx, texts in enumerate(self.mmcorpus) :
            n_words = sum([term[1] for term in texts])
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

    def update_word_dict(self, labels_pred) :
        """ Find Discrimination words. """
        condidate_word = dict().fromkeys(self.dictionary.token2id.values(), None)
        for word in condidate_word :
            condidate_word[word] = [0.0] * self.n_cluster
        cluster_number = [0.0] * self.n_cluster
        for idx, texts in enumerate(self.mmcorpus) :
            n_words = sum([times for word, times in texts])
            if labels_pred[idx] != -1 :
                cluster_number[labels_pred[idx]] += 1
                for word, times in texts :
                    condidate_word[word][labels_pred[idx]] += 1
        for word in condidate_word.keys() :
            for label in range(self.n_cluster) :
                condidate_word[word][label] = 1.0 * (condidate_word[word][label] + 1) / \
                    (cluster_number[label] + len(self.word_dict))
        selected_word = self.select_condidate_word(condidate_word, threshold=0.01)
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
                    score = 1.0 * ((condidate_word[word][label]) ** (self.n_cluster)) / s
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
            selected_word.extend(selected_label_word[0:200])
        return selected_word

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
        adj_labels_pred = {id: int(labels_pred[id])+1 for id in labels_pred.keys()}
        score = 1.0 * sum([1 for id in labels_true \
            if adj_labels_pred[id] == labels_true[id]] ) / len(labels_true)
        print 'accurancy is', score

    def get_doc_topic(self, article_list) :
        """ Get doc_topic_ list.
            doc_topic_ is list [[('id', id), ('topic1', prob1), ..., ('topicK', probK)], 
                                ...
                               ]
        """
        doc_topic_ = []
        for idx, texts in enumerate(self.mmcorpus) :
            n_words = sum([term[1] for term in texts])
            distinguished = False
            scores = [1.0] * self.n_cluster
            for label in range(self.n_cluster) :
                for word, times in texts :
                    if word in self.word_dict :
                        distinguished = True
                        scores[label] *= self.word_dict[word][label]
                scores[label] *= self.prior_prob[label]
            if distinguished :
                tuple_list = []
                tuple_list.append(('id', article_list[idx].id))
                tuple_list.append(('url', article_list[idx].url))
                tuple_list.append(('title', article_list[idx].title))
                for label in range(self.n_cluster) :
                    tuple_list.append(('topic'+str(label+1), scores[label]))
                doc_topic_.append(tuple_list)
        return doc_topic_

    def get_topic_word(self, word_dict) :
        """ Get doc_topic_ list.
            doc_topic_ is list [[('word', word), ('topic1', prob1), ..., ('topicK', probK)], 
                                ...
                               ]
        """
        topic_word_ = []
        for word in word_dict :
            tuple_list = []
            tuple_list.append(('id', word))
            tuple_list.append(('name', self.dictionary[word]))
            for label in range(self.n_cluster) :
                tuple_list.append(('topic'+str(label+1), word_dict[word][label]))
            topic_word_.append(tuple_list)
        return topic_word_

    def process(self, article_list) :
        """ main process of naive bayes. """
        id_index_dict = {article.id: idx for idx, article in enumerate(article_list)}
        self._init_model()
        labels_pred = [-1] * len(article_list)
        self._start_up_labels(labels_pred, article_list)
        for step in range(0, 10) :
            self.read_test_class(article_list, labels_pred)
            self.evaluation()
            self.word_dict = self.update_word_dict(labels_pred)
            labels_pred = [-1] * len(article_list)
            labels_pred = self.allocate_article(labels_pred)
        doc_topic_ = self.get_doc_topic(article_list)
        topic_word_ = self.get_topic_word(self.word_dict)
        return doc_topic_, topic_word_