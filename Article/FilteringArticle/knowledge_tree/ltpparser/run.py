# -*- encoding = gb18030 -*-

# package importing start
import sys

import gensim
from sklearn import metrics

from qa.article_tag import ArticleCluster
from preload.market import PickleMarket
from embedding.word_embed import WordEmbed
from file.file_operator import TextFileOperator
from ltpparser.parsing import SentenceParsing
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, sentences_path, dictionary_path, wordembed_path, word_cluster_path) :
        pred_word_dict = self.run_cluster_words(sentences_path, dictionary_path, wordembed_path)
        true_word_dict, word_list = self.read_word_cluster(word_cluster_path)
        self.evaluation(pred_word_dict, true_word_dict)

    def run_cluster_words(self, sentences_path, dictionary_path, wordembed_path) :
        parser = SentenceParsing()
        word_set = parser.read_word(sentences_path)
        embedor = WordEmbed()
        word2vec = embedor.word_to_vector(type='load', path=wordembed_path)
        loader = PickleMarket()
        dictionary = loader.load_market(dictionary_path)
        index2word = dict((value, key) for key, value in dictionary.iteritems())
        word_dict = dict()
        for word in word_set :
            if word in dictionary :
                word_idx = str(dictionary[word])
                if word_idx in word2vec.index2word and word not in word_dict :
                    word_dict[word] = word2vec[word_idx]
        cluster = ArticleCluster()
        word_dict = cluster._word_clustering(word_dict)
        return word_dict

    def read_word_cluster(self, word_cluster_path) :
        """ Read word cluster.
            Each row is a word.
            column[0] is the name of word.
            column[1] is the cluster seq of word.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(word_cluster_path)
        entry_list = data_list[0]
        word_dict = dict()
        word_list = list()
        for data in data_list[1:] :
            if len(data) >= len(entry_list) :
                word = data[0]
                if word not in word_dict :
                    word_dict[word] = int(data[1])
                    word_list.append(word)
        return word_dict, word_list

    def evaluation(self, pred_word_dict, true_word_dict) :
        """ evaluate the accurancy of the lda model. """
        labels_pred, labels_true = list(), list()
        for word in pred_word_dict :
            if word in true_word_dict :
                labels_pred.append(pred_word_dict[word])
                labels_true.append(true_word_dict[word])
        score = metrics.adjusted_rand_score(labels_true, labels_pred)  
        print 'adjusted_rand_score is', score
        score = metrics.adjusted_mutual_info_score(labels_true, labels_pred)  
        print 'adjusted_mutual_info_score is', score
        score = metrics.homogeneity_score(labels_true, labels_pred)  
        print 'homogeneity_score is', score
        score = metrics.completeness_score(labels_true, labels_pred)  
        print 'completeness_score is', score