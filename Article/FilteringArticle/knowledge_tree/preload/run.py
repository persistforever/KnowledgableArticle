# -*- encoding = gb18030 -*-

# package importing start
import sys

import gensim

from preload.market import PickleMarket, JsonMarket
from basic.word import Word
from file.file_operator import TextFileOperator
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, sentence_path, market_path) :
        """ function for script to drive. """
        self.run_load_market(market_path)

    def run_create_market(self, sentence_path, market_path) :
        sentences = self.read_sentences(sentence_path)
        loader = PickleMarket()
        market = loader.dump_market(sentences, market_path)

    def run_load_market(self, market_path) :
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