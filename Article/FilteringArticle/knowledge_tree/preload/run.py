﻿# -*- encoding = gb18030 -*-

# package importing start
import sys

import gensim

from preload.market import PickleMarket, JsonMarket
from basic.word import Word
from word.word_bag import DictWordBag, GensimWordBag
from file.file_operator import TextFileOperator
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, sentence_path, dictionary_path, market_path) :
        """ function for script to drive. """
        self.run_create_market(sentence_path, dictionary_path, market_path)
        # self.run_load_market(market_path, dictionary_path)

    def run_create_market(self,  sentence_path, dictionary_path, market_path) :
        sentences = self.read_sentences(sentence_path)
        embedor = DictWordBag()
        dictionary = embedor.dump_dictionary(sentences, dictionary_path)
        converted_sentences = self.convert_sentences(sentences, dictionary)
        loader = PickleMarket()
        market = loader.dump_market(converted_sentences, market_path)

    def run_load_market(self, market_path, dictionary_path) :
        loader = PickleMarket()
        market = loader.load_market(market_path)
        return market

    def read_sentences(self, source_path) :
        """ Read participle sentences.
            Each row is a sentence.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(source_path)
        entry_list = data_list[0]
        sentences = list()
        length = len(data_list[1:]) - 1
        for idx, data in enumerate(data_list[1:]) :
            if len(data) >= len(entry_list) :
                sentence = [Word(word, sp_char=':').to_string() for word in data[0].split(' ')]
                sentences.append(sentence)
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return sentences

    def convert_sentences(self, sentences, dictionary) :
        """ Convert each word in sentences.
            Before convert, word is name<:>pos.
            After convert, word is seq according to dictionary.
        """
        converted_sentences = []
        for sentence in sentences :
            converted_sentence = []
            for word in sentence :
                seq = str(dictionary[word])
                converted_sentence.append(seq)
            converted_sentences.append(converted_sentence)
        return converted_sentences