# -*- encoding = gb18030 -*-

# package importing start
import re

import gensim

from preload.market import PickleMarket
# package importing end


class BaseWordBag :

    def __init__(self) :
        pass

    def load_dictionary(self, path) :
        """ Load the word dictionary from the file. """

    def dump_dictionary(self, sentences, path) :
        """ Dump the word dictionary using sentences. """


class GensimWordBag(BaseWordBag) :
    import gensim

    def __init__(self) :
        pass

    def load_dictionary(self, path) :
        """ Load the word dictionary from the file. """
        dictionary = gensim.corpora.Dictionary.load(path)
        print dictionary
        return dictionary

    def dump_dictionary(self, dict, path) :
        """ Dump the word dictionary using sentences. """
        dictionary = gensim.corpora.Dictionary()
        dictionary.token2id = dict
        dictionary.save(path)
        print dictionary
        return dictionary


class DictWordBag(BaseWordBag) :

    def __init__(self) :
        pass

    def load_dictionary(self, path) :
        """ Load the word dictionary from the file. """
        loader = PickleMarket()
        word2index = loader.load_market(path)
        print 'dictionary size is %d' % len(word2index)
        return word2index

    def dump_dictionary(self, sentences, path) :
        """ Dump the word dict using sentences. """
        word2index = dict()
        for sentence in sentences :
            for word in sentence :
                if word not in word2index :
                    word2index[word] = 0
        for idx, word in enumerate(word2index.keys()) :
            word2index[word] = idx
        loader = PickleMarket()
        loader.dump_market(word2index, path)
        print 'dictionary size is %d' % len(word2index)
        return word2index