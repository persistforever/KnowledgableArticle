﻿# -*- encoding = gb18030 -*-

# package importing start
import sys
import random
import math

import gensim

from tag.robot import Robot
from basic.word import Word
from file.file_operator import TextFileOperator
from preload.market import PickleMarket
# package importing end

class Corpus :

    def __init__(self) :
        pass

    def run(self, sentences_path, tag_tree_path, sentences_market_path, tags_path) :
        self.run_tag_sentences(tag_tree_path, sentences_path, sentences_market_path, tags_path)
        # self.run_robot(tag_tree_path, sentences_market_path, tags_path)
        # self.test_entropy()

    def run_tag_sentences(self, tag_tree_path, sentences_path, sentences_market_path, tags_path) :
        robot = Robot()
        tag_tree = robot.read_tag_tree(tag_tree_path)
        sentences = self.read_sentences(sentences_path)
        tags = robot.tag_sentences(tag_tree, sentences)
        loader = PickleMarket()
        self.write_tags(sentences, tags, tags_path)
        # loader.dump_market(tags, tags_path)
        loader.dump_market(sentences, sentences_market_path)

    def run_robot(self, tag_tree_path, sentences_market_path, tags_path) :
        robot = Robot()
        loader = PickleMarket()
        tag_tree = robot.read_tag_tree(tag_tree_path)
        sentences = loader.load_market(sentences_market_path)
        tags = loader.load_market(tags_path)
        print 'start'
        string = raw_input().decode('gb18030')
        # string = u'我想要毛衣'
        sentences = robot.question_and_answer(string, sentences, tags)

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
                sentence = data[0]
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

    def test_entropy(self) :
        for step in range(0, 10) :
            n = random.randint(5,21)
            array = [0.0] * 1000
            for t in range(len(array)) :
                rd = random.random()
                if rd <= 0.5 :
                    array[t] = 1
                elif rd <= 0.85 :
                    array[t] = 2
                else :
                    array[t] = random.randint(3, n)
            h_array = [0.0] * (n+1)
            entropy_list = list()
            for x in range(1, n+1) :
                p = 1.0 * len([a for a in array if a == x]) / len(array)
                if p == 0 :
                    h_array[x] = 0.0
                else :
                    h_array[x] = -1.0 * p * math.log(p)
                entropy_list.append([x, h_array[x]])
            sorted_array = sorted(entropy_list, key=lambda x:x[1], reverse=True)
            for x, h in sorted_array[0:] :
                print x, h
            print 
            stringa = str(sorted_array[0][0])
            stringb = str(sorted_array[1][0])
            stringc = str(sorted_array[2][0])
            string1 = ''.join(sorted([stringa, stringb, stringc]))
            sum_list = list()
            for x in range(1, n+1) :
                for y in range(x+1, n+1) :
                    for z in range(x+1, n+1) :
                        h_x = h_array[x]
                        h_y = h_array[y]
                        h_z = h_array[z]
                        p_o = 1.0 * len([a for a in array if a != x and a != y and a != z]) / len(array)
                        h_o= -1.0 * p_o * math.log(p_o)
                    sum_list.append([x, y, z, h_x + h_y + h_z + h_o])
            term = max(sum_list, key=lambda x: x[3])
            print term[0], term[1], term[2], term[3]
            print '-'*50
            stringa = str(term[0])
            stringb = str(term[1])
            stringc = str(term[2])
            string2 = ''.join(sorted([stringa, stringb, stringc]))
            if string1 != string2 :
                print 'failed!'
                return
        print 'succes!'