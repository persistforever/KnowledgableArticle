# -*- encoding = gb18030 -*-

# package importing start
import sys

import gensim

from basic.market import PickleMarket
from embedding.word_embed import WordEmbed
from basic.word import Word
from file.file_operator import TextFileOperator
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, sentences_path, dictionary_path, wordembed_path, word_cluster_path, \
        similarity_path, wordvector_path) :
        # self.run_create_word2vec(sentences_path, dictionary_path, wordembed_path)
        # self.run_evaluate_word2vec(wordembed_path, dictionary_path, word_cluster_path, \
        #     similarity_path)
        # self.run_remove_stopwords(sentences_path, dictionary_path)
        self.run_write_wordvector(wordembed_path, dictionary_path, wordvector_path)

    def run_create_word2vec(self, sentence_path, dictionary_path, \
        wordembed_path) :
        loader = PickleMarket()
        sentences = loader.load_market(sentence_path)
        # sentences = self.run_remove_stopwords(sentence_path, dictionary_path)
        embedor = WordEmbed()
        word2vec = embedor.word_to_vector(type='create', sentences=sentences, path=wordembed_path)

    def run_write_wordvector(self, wordembed_path, dictionary_path, wordvecotr_path) :
        embedor = WordEmbed()
        word2vec = embedor.word_to_vector(type='load', path=wordembed_path)
        loader = PickleMarket()
        dictionary = loader.load_market(dictionary_path)
        index2word = dict((value, key) for key, value in dictionary.iteritems())
        self.write_word_vector(word2vec, index2word, wordvecotr_path)
        return word2vec

    def write_word_vector(self, word2vec, index2word, wordvector_path) :
        """ Write word vector.
            Each row is a word.
            Column[0] is the name of word.
            Column[1:] is the entry of the word vector.
        """
        file_operator = TextFileOperator()
        data_list = list()
        for index in index2word :
            if str(index) in word2vec.vocab :
                data = [index2word[index]]
                data.extend(word2vec[str(index)])
                data_list.append(data)
        file_operator.writing(data_list, wordvector_path)

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