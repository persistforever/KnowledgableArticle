# -*- encoding = gb18030 -*-

# package importing start
import re

import gensim

from file.file_operator import TextFileOperator
# package importing end


class WordBag :

    def __init__(self) :
        pass

    def word_to_dictionary(self, type='create', sentences=[], path='') :
        """ If type is 'create' :
                Initialize the word dictionary using sentences.
            If type is 'load' :
                Initialize the word dictionary from the file.
        """
        if type is 'create' :
            dictionary = gensim.corpora.Dictionary(sentences)
            dictionary.save(path)
        elif type is 'load' :
            dictionary = gensim.corpora.Dictionary.load(path)
        print dictionary
        return dictionary