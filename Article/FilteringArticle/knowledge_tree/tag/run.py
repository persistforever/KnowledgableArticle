# -*- encoding = gb18030 -*-

# package importing start
import sys
import random
import math

import gensim

from tag.robot import Robot
from tag.tag_tree import TagTree
from file.file_operator import TextFileOperator
from preload.market import PickleMarket
# package importing end

class Corpus :

    def __init__(self) :
        pass

    def run(self, sentences_path, tag_tree_path, sentences_market_path, tags_path, \
        tags_martket_path, untag_sentence_path) :
        # self.run_convert_sentences(sentences_path, sentences_market_path)
        self.run_tag_sentences(tag_tree_path, sentences_market_path, tags_path, \
            tags_martket_path, untag_sentence_path)
        # self.run_robot(tag_tree_path, sentences_market_path, tags_path)

    def run_convert_sentences(self, sentences_path, sentences_market_path) :
        file_operator = TextFileOperator()
        sentences = self.read_sentences(sentences_path)
        loader = PickleMarket()
        loader.dump_market(sentences, sentences_market_path)

    def run_tag_sentences(self, tag_tree_path, sentences_market_path, tags_path, \
        tags_martket_path, untag_sentence_path) :
        file_operator = TextFileOperator()
        loader = PickleMarket()
        sentences = loader.load_market(sentences_market_path)
        cmd_list = file_operator.reading(tag_tree_path)
        tag_tree = TagTree(cmd_list)
        robot = Robot()
        tags, untag_sentences = robot.tag_sentences(tag_tree, sentences[0:10000])
        loader = PickleMarket()
        self.write_tags(sentences, tags, tags_path)
        loader.dump_market(tags, tags_martket_path)
        file_operator.writing(untag_sentences, untag_sentence_path)
        # loader.dump_market(untag_sentences, sentences_market_path)
        print '%.2f%% article >= 2 tags' % (100.0 * len([tag for tag in tags if len(tag) >= 2]) / len(tags))
        print '%.2f%% article >= 3 tags' % (100.0 * len([tag for tag in tags if len(tag) >= 3]) / len(tags))

    def run_robot(self, tag_tree_path, sentences_market_path, tags_path) :
        robot = Robot()
        loader = PickleMarket()
        file_operator = TextFileOperator()
        cmd_list = file_operator.reading(tag_tree_path)
        tag_tree = TagTree(cmd_list)
        sentences = loader.load_market(sentences_market_path)
        tags = loader.load_market(tags_path)
        print 'start'
        string = raw_input().decode('gb18030')
        # string = u'我想要毛衣'
        sentences = robot.question_and_answer(string, sentences, tags, tag_tree)

    def read_sentences(self, sentences_path) :
        """ Read participle sentences.
            Each row is a sentence.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(sentences_path)
        entry_list = data_list[0]
        sentences = list()
        length = len(data_list[1:]) - 1
        for idx, data in enumerate(data_list[1:]) :
            if len(data) >= len(entry_list) :
                sentence = data[0].upper()
                sentences.append(sentence)
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return sentences

    def write_tags(self, sentences, tags, tags_path) :
        """ Read participle sentences.
            Each row is a sentence.
            Each column is a <attribute, value> pair.
        """
        file_operator = TextFileOperator()
        data_list = list()
        data_list.append(['sentence', 'tag'])
        length = len(tags) - 1
        for idx, term in enumerate(tags) :
            if len(term) >= 2 :
                data = list()
                data.append(sentences[idx])
                tag_str = ''
                for attr, value in term :
                    tag_str += u'<' + attr + u',' + value + u'>' + ' '
                data.append(tag_str)
                data_list.append(data)
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        file_operator.writing(data_list, tags_path)