# -*- encoding = gb18030 -*-
""" Filter the structure word.
        first step : clustering the words.
        second step : filtering the words. """
         
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import numpy as np
from basic.word import Word
from basic.tag import Tag
from basic.article import Article
import file.file_operator as fop
from file.path_manager import PathManager
from tag_tree import TreeNode
import lda


class WordBag :

    def __init__(self) :
        self.word_index = dict()
        self.index_word = dict()
        self.index_article = dict()
        self.path_manager = PathManager()
        self.file_operator = fop.BaseFileOperator()
        self.tag_list = []

    def read_word_bag(self) :
        """ Read word bag.
        Each row of the file is a word. 
        Each column of the word is [word, id]. """

        self.file_operator = fop.TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_tag_wordbag())
        for data in data_list :
            if len(data) >= 2 :
                word = Word(data[0])
                self.index_word[int(data[1])-1] = word
        print 'reading word bag finished ...'

    def read_article_bagofword(self) :
        """ Read bagofword vector of article.
        Each row of the file is a article. 
        Each column of the word is bagofword vector. """

        self.file_operator = fop.TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_tag_bagofword())
        idx = 0 
        for data in data_list[0:1000] :
            if len(data) >= 2 :
                article = Article()
                article.set_params(id=data[0])
                article.import_bagofword(data[1].split(' '))
                self.index_article[idx] = article
                idx += 1
        print 'reading article bagofword finished ...'

    def read_tree(self, tag_name) :
        """ Read tag tree from xml file. """
        dom = xml.dom.minidom.parse(name)
        root = dom.documentElement
        nodeset = root.getElementsByTagName('url')
        urlset = []
        for node in nodeset :
            urlset.append(node.firstChild.data.strip())
        return urlset

    def _constr_tree(self) :
        """ Use LDA model to construct the tree. """
        root_node = TreeNode(1, 4)
        root_node.set_params(article_list = self.index_article.keys())
        word_list = [[word, 1.0] for word in self.index_word.values()]
        root_node.set_params(word_list = word_list)
        self._constr_tree_node(root_node)
        return root_node

    def _constr_tree_node(self, node) :
        """ Use LDA model to construct node of the tree. """
        # exit condition
        node.text = node.print_node()
        print node.text.encode('gb18030')
        self.tag_list.append(Tag(node.get_word_list()))
        if node.level >= 4 :
            return
        print len(node.word_list), len(node.article_list)
        node.split_node(self.index_article, self.index_word)
        for sub_node in node.child_list :
            self._constr_tree_node(sub_node)

    def _running_lda(self) :
        """ Use LDA to obeserve the clustering of article. """
        
        article_list = self.index_article.values()
        article_bagofword = []
        for article in article_list :
            article_bagofword.append(article.bagofword_vector)
        article_bagofword = np.array(article_bagofword)
        model = lda.LDA(n_topics=5, n_iter=400, random_state=1).fit(article_bagofword)
        article_topic_list = []
        for idx in range(model.doc_topic_.shape[0]) :
            topic_list = [article_list[idx].id]
            topic_list.extend([str(t) for t in model.doc_topic_[idx, :].tolist()])
            article_topic_list.append(topic_list)
        word_topic_list = []
        for idx in range(model.topic_word_.shape[1]) :
            word_topic_list.append([str(t) for t in model.topic_word_[:, idx].tolist()])
        return article_topic_list, word_topic_list

    def write_word_topic(self, word_topic_list) :
        """ Write word_topic. 
        Each row of the file is a word. 
        Each column of the file is the weight in each topic of the word. """

        self.file_operator = fop.CSVFileOperator()
        self.file_operator.writing(word_topic_list, self.path_manager.get_tag_wordtopic())

    def write_article_topic(self, article_topic_list) :
        """ Write word_topic. 
        Each row of the file is a word. 
        Each column of the file is the weight in each topic of the word. """

        self.file_operator = fop.CSVFileOperator()
        self.file_operator.writing(article_topic_list, self.path_manager.get_tag_articletopic())

    def write_tree(self, root_node) :
        """ Write tree into XML file. """
        self.file_operator = fop.XmlFileOperator()
        self.file_operator.writing(root_node, self.path_manager.get_tag_tagtree())

    def write_tag_list(self, tag_list) :
        """ Write tree into CSV file. """
        self.file_operator = fop.CSVFileOperator()
        self.file_operator.writing(tag_list, self.path_manager.get_tag_taglist())

    def get_word_bag(self) :
        self.read_word_bag()
        self.read_article_bagofword()
        root_node = self._constr_tree()
        self.write_tree(root_node)
        line_list = self.get_tag_list()
        self.write_tag_list(line_list)

    def observe_lda(self) :
        self.read_word_bag()
        self.read_article_bagofword()
        article_topic_list, word_topic_list = self._running_lda()
        self.write_article_topic(article_topic_list)
        self.write_word_topic(word_topic_list)

    def get_tag_list(self) :
        line_list = []
        for seq, tag in enumerate(self.tag_list) :
            line = [str(seq)]
            for word in tag.word_list :
                line.append(word.toString())
            line_list.append(line)
        return line_list