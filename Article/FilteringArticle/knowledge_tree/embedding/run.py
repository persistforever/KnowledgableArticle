# -*- encoding = gb18030 -*-

# package importing start
import sys

import gensim

from preload.market import PickleMarket
from embedding.word_embed import WordEmbed
from basic.word import Word
from file.file_operator import TextFileOperator
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, sentences_path, dictionary_path, wordembed_path, word_cluster_path, \
        similarity_path, wordvector_path) :
        # self.run_create_word2vec(sentences_path, dictionary_path, wordembed_path)
        # self.run_evaluate_word2vec(wordembed_path, dictionary_path, word_cluster_path, \
        #     similarity_path)
        # self.run_remove_stopwords(sentences_path, dictionary_path)
        self.run_write_wordvector(wordembed_path, dictionary_path, wordvector_path)

    def run_create_word2vec(self, sentence_path, dictionary_path, \
        wordembed_path) :
        loader = PickleMarket()
        sentences = loader.load_market(sentence_path)
        # sentences = self.run_remove_stopwords(sentence_path, dictionary_path)
        embedor = WordEmbed()
        word2vec = embedor.word_to_vector(type='create', sentences=sentences, path=wordembed_path)

    def run_evaluate_word2vec(self, wordembed_path, dictionary_path, word_cluster_path, \
        similarity_path) :
        embedor = WordEmbed()
        word2vec = embedor.word_to_vector(type='load', path=wordembed_path)
        loader = PickleMarket()
        dictionary = loader.load_market(dictionary_path)
        index2word = dict((value, key) for key, value in dictionary.iteritems())
        word_dict, word_list = self.read_word_cluster(word_cluster_path)
        score, similarity_matrix = embedor.evaluate_word2vec_model(dictionary, word2vec, word_dict, word_list)
        self.write_similarity_matrix(word_list, similarity_matrix, similarity_path)
        print 'score of word2vec model is %.4f.' % score
        return word2vec

    def run_remove_stopwords(self, sentence_path, dictionary_path) :
        loader = PickleMarket()
        sentences = loader.load_market(sentence_path)
        dictionary = loader.load_market(dictionary_path)
        embedor = WordEmbed()
        rmstop_sentences = embedor.remove_stop_words( \
            type='load', dictionary=dictionary, sentences=sentences)
        return rmstop_sentences

    def run_write_wordvector(self, wordembed_path, dictionary_path, wordvecotr_path) :
        embedor = WordEmbed()
        word2vec = embedor.word_to_vector(type='load', path=wordembed_path)
        loader = PickleMarket()
        dictionary = loader.load_market(dictionary_path)
        index2word = dict((value, key) for key, value in dictionary.iteritems())
        self.write_word_vector(word2vec, index2word, wordvecotr_path)
        return word2vec

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

    def write_similarity_matrix(self, word_list, similarity_matrix, similarity_path) :
        """ Write similarity matrix.
            Each row and column is a word.
            Each entry in matrix is the similarity.
        """
        file_operator = TextFileOperator()
        data_list = []
        data = ['sim']
        data.extend(word_list)
        data_list.append(data)
        for row in range(similarity_matrix.shape[0]) :
            data = [word_list[row]]
            data.extend(similarity_matrix[row, :].tolist())
            data_list.append(data)
        file_operator.writing(data_list, similarity_path)

    def write_word_vector(self, word2vec, index2word, wordvector_path) :
        """ Write word vector.
            Each row is a word.
            Column[0] is the name of word.
            Column[1:] is the entry of the word vector.
        """
        file_operator = TextFileOperator()
        data_list = list()
        for index in index2word :
            if str(index) in word2vec.vocab :
                data = [index2word[index]]
                data.extend(word2vec[str(index)])
                data_list.append(data)
        file_operator.writing(data_list, wordvector_path)