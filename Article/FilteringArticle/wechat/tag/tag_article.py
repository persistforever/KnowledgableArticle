# -*- encoding = gb18030 -*-
""" Tag article use tag_list from the word_bag. """
         
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import file.file_operator as fop
from file.path_manager import PathManager
from tag_tree import TreeNode
from basic.tag import Tag
from basic.word import Word
from gensim import models


class Tagger :

    def __init__(self) :
        self.tag_list = []
        self.path_manager = PathManager()
        self.file_operator = fop.BaseFileOperator()

    def read_tag_list(self) :
        """ Read tag_list from input/tag_list.
        Each row of the file is a tag.
        column[0] of the file is the id of the tag.
        Each column[1:] of the file is the word in the tag. """

        self.file_operator = fop.CSVFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_output_taglist())
        for data in data_list :
            word_list = []
            for wd in data[1:] :
                word_list.append(Word(wd))
            tag = Tag(word_list, seq=int(data[0]))
            self.tag_list.append(tag)
        print 'reading tag_list finished ...'

    def tag_article_list(self, article_list) :
        """ use tag_list to tag article_list(simpliyfied by its top 20 keyword). """
        for article in article_list :
            article.tag_list = []
            for tag in self.tag_list :
                for article_word, tfidf in article.keyword_list :
                    if article_word.toString() in [word.toString() for word in tag.word_list] :
                        article.tag_list.append(tag.seq)
                        break