# -*- encoding = gb18030 -*-

# package importing start
import sys

import gensim

from preload.market import PickleMarket
from word.word_bag import DictWordBag
from basic.word import Word
from file.file_operator import TextFileOperator
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, sentence_path, dictionary_path, converted_sentence_path) :
        self.run_create_dictionary(sentence_path, dictionary_path, converted_sentence_path)
        # self.run_load_dictionary(dictionary_path, converted_sentence_path)

    def run_create_dictionary(self, sentence_path, \
        dictionary_path, converted_sentence_path) :
        sentences = self.read_sentences(sentence_path)
        embedor = WordBag()
        dictionary = embedor.dump_word_dict(sentences=sentences, path=dictionary_path)
        converted_sentences = self.convert_sentences(sentences, dictionary)
        loader = PickleMarket()
        loader.dump_market(converted_sentences, converted_sentence_path)

    def run_load_dictionary(self, dictionary_path, converted_sentence_path) :
        embedor = WordBag()
        dictionary = embedor.word_to_dictionary(type='load', path=dictionary_path)
        loader = PickleMarket()
        converted_sentences = loader.load_market(converted_sentence_path)
        return dictionary, converted_sentences

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