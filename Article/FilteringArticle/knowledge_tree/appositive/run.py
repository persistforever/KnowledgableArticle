# -*- encoding = gb18030 -*-

# package importing start
import sys

import gensim

from appositive.word_apposit import Appositive
from basic.word import Word
from file.file_operator import TextFileOperator
# package importing end

class Corpus :

    def __init__(self) :
        pass

    def run(self, sentences_path, wordembed_path, appositive_path) :
        self.run_find_appositive(sentences_path, wordembed_path, appositive_path)

    def run_find_appositive(self, sentences_path, wordembed_path, appositive_path) :
        seed = u'裤'
        sentences = self.read_sentences(sentences_path)
        appositive = Appositive()
        word_dict = appositive.find_appositive(seed, sentences)
        return word_dict

    def read_sentences(self, sentences_path) :
        """ Read participle sentences.
            Each row is a sentence.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(sentences_path)
        entry_list = data_list[0]
        sentences = list()
        for idx, data in enumerate(data_list[1:]) :
            if len(data) >= len(entry_list) :
                sentence = [Word(word, sp_char=':') for word in data[0].split(' ')]
                sentences.append(sentence)
        return sentence