# -*- encoding = gb18030 -*-

# package importing start
import re

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

    def dump_dictionary(self, sentences, path) :
        """ Dump the word dictionary using sentences. """
        dictionary = gensim.corpora.Dictionary(sentences)
        dictionary.save(path)
        print dictionary
        return dictionary


class DictWordBag(BaseWordBag) :

    def __init__(self) :
        pass

    def load_dict(self, path) :
        """ Load the word dictionary from the file. """
        loader = PickleMarket()
        word2index = loader.load_market(path)
        print word2index
        return word2index

    def dump_dict(self, sentences, path) :
        """ Dump the word dict using sentences. """
        word2index = dict()
        index = 0
        for sentence in sentences :
            for word in sentence :
                if word not in dict :
                    word2index[word] = index
                    index += 1
        loader = PickleMarket()
        loader.dump_market(word2index, path)
        return word2index