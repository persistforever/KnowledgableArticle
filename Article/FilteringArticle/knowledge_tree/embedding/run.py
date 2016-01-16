# -*- encoding = gb18030 -*-

# package importing start
import sys

import gensim

from basic.market import PickleMarket
from embedding.word_embed import WordEmbed
from basic.word import Word
from file.file_operator import TextFileOperator
from basic.market import PickleMarket
from pretreate.segementor import ContentSegementor
from pretreate.unique import Unique
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, article_path, participle_title_path, sentences_path, sentences_market_path, \
        word_embedding_path, word_embedding_market_path) :
        # self.run_create_sentences(article_path, participle_title_path, sentences_path)
        # self.run_convert_sentences(sentences_path, sentences_market_path)
        self.run_create_word2vec(sentences_market_path, word_embedding_path, word_embedding_market_path)

    def run_create_sentences(self, article_path, participle_title_path, sentences_path) :
        articles = self.read_article(article_path)
        titles = self.read_participle_title(participle_title_path)

        # remove duplications
        processor = Unique()
        indexs_unique = [titles[index]['id'] for index in processor.unique( \
            [article['participle_title'] for article in titles])]
        indexs_dict = dict().fromkeys(set(indexs_unique))
        remained_articles = [article for article in articles if article['id'] in indexs_dict]
        print 'remove duplications finished ...'

        # create sentences
        segmentor = ContentSegementor()
        sentences = list()
        length = len(remained_articles) - 1
        for idx, article in enumerate(remained_articles) :
            segmented_content = segmentor.segement(article['content'])
            sentences.extend([[sentence] for sentence in segmented_content])
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        
        file_operator = TextFileOperator()
        file_operator.writing(sentences, sentences_path)
        print 'writing sentences finished ...'
        
    def run_convert_sentences(self, sentences_path, sentences_market_path) :
        file_operator = TextFileOperator()
        sentences = file_operator.reading(sentences_path)
        sentences = [[word.split('<:>')[0] for word in sentence] for sentence in sentences]
        loader = PickleMarket()
        loader.dump_market(sentences, sentences_market_path)
        print 'converting sentences finished ...'

    def run_create_word2vec(self, sentences_path, word_embedding_path, word_embedding_market_path) :
        loader = PickleMarket()
        sentences = list()
        for type in [u'_car']:#, u'_finance', u'_web'] :
            sentences.extend(loader.load_market(sentences_path + type))
        print 'import finish ...'
        embeddor = WordEmbed()
        print sentences[0]
        model = embeddor.word_to_vector(type='create', sentences=sentences[0:100], path=word_embedding_market_path)
        data_list = embeddor.get_word2vec_model(model)
        file_operator = TextFileOperator()
        file_operator.writing(data_list, word_embedding_path)
        print 'create word2vec finished ...'

    def read_article(self, article_path) :
        """ Read source article.
            Each row is an article.
            Colunm[0] is the id of article.
            Column[1:] is the attributes of article.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(article_path)
        entry_list = data_list[0]
        source_list = []
        length = len(data_list[1:]) - 1
        for idx, data in enumerate(data_list[1:]) :
            if len(data) >= len(entry_list) :
                article = dict()
                article['id'] = data[0]
                article['url'] = data[1]
                article['pub_time'] = data[2]
                article['title'] = data[3]
                article['content'] = data[4]
                article['n_zan'] = data[5]
                article['n_forward'] = data[6]
                article['n_click'] = data[7]
                article['n_collect'] = data[8]
                article['read_time'] = data[9]
                article['finish_rate'] = data[10]
                source_list.append(article)
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return source_list

    def read_participle_title(self, title_path) :
        """ Read participle title.
            Each row is an article.
            Colunm[0] is the id of article.
            Column[1:] is the word of participle title.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(title_path)
        entry_list = data_list[0]
        source_list = list()
        length = len(data_list[1:]) - 1
        for idx, data in enumerate(data_list[1:]) :
            if len(data) >= len(entry_list) :
                article = dict()
                article['id'] = data[0]
                article['participle_title'] = [Word(word) for word in data[1].split(' ')]
                source_list.append(article)
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return source_list

    def read_sentences(self, source_path, type='all') :
        """ Read participle sentences.
            Each row is a sentence.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(source_path)
        entry_list = data_list[0]
        sentences = list()
        length = len(data_list[1:]) - 1
        if type == 'all' :
            for idx, data in enumerate(data_list[1:]) :
                if len(data) >= len(entry_list) :
                    sentence = [Word(word, sp_char=':').to_string() for word in data[0].split(' ')]
                    sentences.append(sentence)
                if idx % 100 == 0 :
                    print 'finish rate is %.2f%%\r' % (100.0*idx/length),
            print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        elif type == 'name' :
            for idx, data in enumerate(data_list[1:]) :
                if len(data) >= len(entry_list) :
                    sentence = [Word(word, sp_char=':').name for word in data[0].split(' ')]
                    sentences.append(sentence)
                if idx % 100 == 0 :
                    print 'finish rate is %.2f%%\r' % (100.0*idx/length),
            print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return sentences

    def create_dictionary(self, sentences, type='all') :
        """ Create word dict using sentences. """
        word2index = dict()
        if type == 'all' :
            for sentence in sentences :
                for word in sentence :
                    if word not in word2index :
                        word2index[word] = 0
        elif type == 'name' :
            for sentence in sentences :
                for word in sentence :
                    if word.name not in word2index :
                        word2index[word.name] = 0
        for idx, word in enumerate(word2index.keys()) :
            word2index[word] = idx
        print 'dictionary size is %d' % len(word2index)
        return word2index

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