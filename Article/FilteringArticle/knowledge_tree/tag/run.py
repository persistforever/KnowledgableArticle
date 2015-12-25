# -*- encoding = gb18030 -*-

# package importing start
import sys

import gensim

from tag.tagger import Tagger
from basic.word import Word
from file.file_operator import TextFileOperator
# package importing end

class Corpus :

    def __init__(self) :
        pass

    def run(self, sentences_path, tag_tree_path, tags_path) :
        self.run_tag_sentences(tag_tree_path, sentences_path, tags_path)

    def run_tag_sentences(self, tag_tree_path, sentences_path, tags_path) :
        tagger = Tagger()
        tag_tree = tagger.read_tag_tree(tag_tree_path)
        sentences = self.read_sentences(sentences_path)
        tag_list = tagger.tag_sentences(tag_tree, sentences)
        self.write_tags(tag_list, tags_path)

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

    def write_tags(self, tag_list, tags_path) :
        """ Read participle sentences.
            Each row is a sentence.
            Each column is a <attribute, value> pair.
        """
        file_operator = TextFileOperator()
        data_list = list()
        data_list.append(['sentence', 'tag'])
        length = len(tag_list) - 1
        for idx, term in enumerate(tag_list) :
            if term[1] != list() :
                data = list()
                data.append(term[0])
                tag_str = ''
                for attr, value in term[1] :
                    tag_str += u'<' + attr + u',' + value + u'>' + ' '
                data.append(tag_str)
                data_list.append(data)
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        file_operator.writing(data_list, tags_path)