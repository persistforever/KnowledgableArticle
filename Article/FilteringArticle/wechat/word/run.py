﻿# -*- encoding = gb18030 -*-

# package importing start
import sys

import gensim

from word.word_bag import WordBag
from basic.word import Word
from file.file_operator import TextFileOperator
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run_create_dictionary(self, sentence_path, \
        dictionary_path) :
        sentences = self.read_sentences(sentence_path)
        embedor = WordBag()
        word2vec = embedor.word_to_dictionary(type='create', sentences=sentences, path=dictionary_path)

    def read_sentences(self, source_path) :
        """ Read participle sentences.
            Each row is a sentence.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(source_path)
        entry_list = data_list[0]
        sentences = list()
        for data in data_list[1:] :
            if len(data) >= len(entry_list) :
                sentence = [Word(word, sp_char=':').to_string() for word in data[0].split(' ')]
                sentences.append(sentence)
        return sentences