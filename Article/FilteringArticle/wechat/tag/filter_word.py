# -*- encoding = gb18030 -*-
""" Filter the structure word.
        first step : clustering the words.
        second step : filtering the words. """
         
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from basic.word import Word
from file.file_operator import TextFileOperator
from file.path_manager import PathManager


class WordBag :

    def __init__(self) :
        self.word_bag = dict()
        self.path_manager = PathManager()
        self.file_operator = BaseFileOperator()

    def read_word_bag(self) :
        """ Read word bag from file named 'wordbag.txt'.
        Each row of the file is a word. 
        Each column of the word is [word, id]. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_input_wordbag())
        for data in data_list :
            if len(data) >= 2 :
                word = Word(data[0])
                self.word_bag[word]

    def get_word_bag(self) :
        self.read_word_bag()
        return self.word_bag