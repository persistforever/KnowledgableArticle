# -*- encoding = gb18030 -*-

# package importing start
import sys

import gensim

from preload.json_market import JsonMarket
from embedding.word_embed import WordEmbed
from basic.word import Word
from file.file_operator import TextFileOperator
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run_create_word2vec(self, sentence_path, \
        word2vec_path) :
        # sentences = self.read_sentences(sentence_path)
        sentences = self.read_sentences_json(sentence_path)
        embedor = WordEmbed()
        word2vec = embedor.word_to_vector(type='create', sentences=sentences, path=word2vec_path)

    def run_evaluate_word2vec(self, word2vec_path, word_cluster_path) :
        embedor = WordEmbed()
        word2vec = embedor.word_to_vector(type='load', path=word2vec_path)
        word_dict = self.read_word_cluster(word_cluster_path)
        score = embedor.evaluate_word2vec_model(word2vec, word_dict)
        print 'score of word2vec model is ', score
        return word2vec

    def read_sentences_json(self, sentence_path) :
        loader = JsonMarket()
        sentences = loader.sentences_to_json(type='load', path=sentence_path)
        return sentences

    def read_sentences(self, sentence_path) :
        """ Read participle sentences.
            Each row is a sentence.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(sentence_path)
        entry_list = data_list[0]
        sentences = list()
        for data in data_list[1:] :
            if len(data) >= len(entry_list) :
                sentence = [Word(word, sp_char=':').to_string() for word in data[0].split(' ')]
                sentences.append(sentence)
        return sentences

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
        for data in data_list[1:] :
            if len(data) >= len(entry_list) :
                word = data[0]
                if word not in word_dict :
                    word_dict[word] = int(data[1])
        return word_dict
