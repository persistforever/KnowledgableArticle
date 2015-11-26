# -*- encoding = gb18030 -*-
""" Class corpus """
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import math
import numpy as np
from article import Article
from article import Word
from file.file_operator import BaseFileOperator, CSVFileOperator, TextFileOperator
from file.path_manager import PathManager
from classifier.unsupervised_classifier import MultiConditionClassifier
from classifier.supervised_classifier import SvmClassifier
from simplifier.title_simplifier import TitleSimplifier


############################################################################
class Corpus :

    def __init__(self) :
        self.article_list = []
        self.path_manager = PathManager()
        self.file_operator = BaseFileOperator()

    def read_article_list(self) :
        """ Read article list from output/article.
        Each row of the file is a article.
        Each column of the file is the attributes of article. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_classify_article())
        for data in data_list :
            if len(data) >= 4 :
                article = Article()
                article.import_article(data)
                self.article_list.append(article)
        print 'reading article list finished ...'
        self._constr_dict_id()

    def read_train_dataset(self) :
        """ Read train_dataset from input/traindata.
        Each row of the file is a article.
        Each column[0:3] of the file is the attributes of the article. 
        Each column[3:-1] of the file is the feature of the article. 
        column[-1] of the file is the label of the article. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_classify_traindataset())
        dataset_list = [np.array(line[3:-1]) for line in data_list]
        label_list = [line[-1] for line in data_list]
        self.train_dataset = self._normalization(np.array(dataset_list, dtype=float))
        self.train_label = np.array(label_list, dtype=float)
        print 'reading train dataset finished ...'

    def read_test_dataset(self) :
        """ Read test_dataset from input/traindata.
        Each row of the file is a article.
        column[0] of the file is the id of the article.
        Each column[1:] of the file is the feature of the article. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_classify_testdataset())
        test_dataset = np.array([np.array(line[1:]) for line in data_list], dtype=float)
        self.test_dataset = self._normalization(test_dataset)
        for idx in range(len(data_list)) :
            id = data_list[idx][0]
            if id in self._id_article :
                self._id_article[id].import_feature_set(list(self.test_dataset[idx]))
        print 'reading test dataset finished ...'

    def read_knowledgeable(self) :
        """ Read knowledgeable article.
        Each row of the file is a article.
        column[0] of the file is the id of the article.
        Each column[1:] of the file is the attributes of the article. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_classify_knowledgeable())
        for data in data_list :
            if len(data) >= 4 :
                article = Article()
                article.import_article(data)
                self.article_list.append(article)
        print 'reading keyword finished ...'
        self._constr_dict_id()

    def read_qa_article(self, rate=0.1) :
        """ Read simplified knowledgeable article.
        Each row of file is article.
        Each column of file is the attributes of the article. """
        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_qa_articl())
        for data in data_list :
            if len(data) >= 4 :
                article = Article()
                article.import_article(data)
                self.article_list.append(article)
        print 'wrirting simply knowledgeable article finished ...'
        self._constr_dict_id()

    def read_keyword(self) :
        """ Read key_word from input/keyword.
        Each row of the file is a article.
        column[0] of the file is the id of the article.
        Each column[1:] of the file is the keyword of the article. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_classify_keyword())
        for data in data_list :
            id = data[0]
            if id in self._id_article :
                self._id_article[id].import_keyword(data, length=100)
        print 'reading keyword finished ...'

    def read_sub_title(self) :
        """ Read sub title of a article.
        Each row of the file is a sub title.
        column[0] of the file is the id of the article.
        column[1] of the file is the sub title. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_classify_subtitle())
        for data in data_list :
            if len(data) >= 2 :
                id = data[0]
                if id in self._id_article :
                    self._id_article[id].import_sub_title(data)
        print 'reading sub title finished ...'

    def read_sub_sentence(self) :
        """ Read sub sentence of a article.
        Each row of the file is a sub sentence.
        column[0] of the file is the id of the article.
        column[1] of the file is the sub sentence. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_qa_subsentence())
        for data in data_list :
            if len(data) >= 2 :
                id = data[0]
                if id in self._id_article :
                    self._id_article[id].import_sub_sentence(data)
        print 'reading sub sentence finished ...'
    
    def classifying(self, seq=1) :
        """ Classify the article_list into knowledgeable and unknowledgeable.
        Return the sorted article_list and top of which is knowledgeable. """

        if seq == 1 :
            classifier = MultiConditionClassifier()
            self.sorted_article_list = classifier.sorting(self.article_list)
        elif seq == 2 :
            classifier = SvmClassifier()
            self.sorted_article_list = classifier.sorting( \
                self.train_dataset, self.train_label, self.article_list)
            self.write_support_vecotrs(classifier.support_index_list)
            self._gzh_sorting()
        print 'classifying article_list finished ...'
    
    def title_simplifying(self, seq=1) :
        """ Simplify the title of the article. """

        simplifier = TitleSimplifier()
        simplifier.model_simplifying(self.article_list)
        print 'simplifying title finished ...'

    def write_knowledgeable_article(self, rate=0.1) :
        """ Write knowledgeable article into output/knowledgeable.
        Each row of file is article.
        Each column of file is the attributes of the article. """
        self.file_operator = CSVFileOperator()
        length = int(len(self.sorted_article_list) * rate)
        data_list = []
        for article in self.sorted_article_list[0:length] :
            data_list.append(article.get_article())
        self.file_operator.writing(data_list, self.path_manager.get_classify_knowledgable())
        print 'wrirting knowledgeable article finished ...'

    def write_simply_knowledgeable_article(self, rate=0.1) :
        """ Write simplified knowledgeable article.
        Each row of file is article.
        Each column of file is the attributes of the article. """
        self.file_operator = TextFileOperator()
        data_list = []
        for article in self.article_list :
            data_list.append(article.get_simply_article())
        self.file_operator.writing(data_list, self.path_manager.get_classify_simplyknowledgeable())
        print 'wrirting knowledgeable article finished ...'

    def write_tag_list(self) :
        """ Write tag list of article.
        Each row of file is an article.
        Each column of file is the tags of the article. """
        self.file_operator = CSVFileOperator()
        data_list = []
        for article in self.article_list :
            data_list.append(article.get_tag_list())
        self.file_operator.writing(data_list, self.path_manager.get_tag_article_tag())
        print 'wrirting article tag_list finished ...'

    def write_support_vecotrs(self, support_index_list) :
        """ Write support vectors into a csv file.
        Each row of file is a support vector.
        Each column of file is the attributes of the support vector. """
        self.file_operator = CSVFileOperator()
        data_list = []
        for idx in support_index_list :
            data = []
            data.extend(self.article_list[idx].get_article())
            data.extend(self.article_list[idx].get_feature_set())
            data_list.append(data)
        self.file_operator.writing(data_list, self.path_manager.get_classify_supportvector())
        print 'wrirting support vectors finished ...'


    def _constr_dict_id(self) :
        """ Construct id_article dict.
        key is id, value is Article object. """
        self._id_article = dict()
        for article in self.article_list :
            if article.id not in self._id_article :
                self._id_article[article.id] = article
        print 'constructing _id_article dict finished ...'

    def _normalization(self, dataset) :
        """ Normalize dataset using mapminmax method. """
        normal_dataset = np.zeros(shape=(dataset.shape[0], dataset.shape[1]))
        for row in range(dataset.shape[0]) :
            for col in range(dataset.shape[1]) :
                normal_dataset[row, col] = dataset[row, col]
        for col in range(normal_dataset.shape[1]) :
            maximum = max(normal_dataset[:, col])
            minimum = min(normal_dataset[:, col])
            for row in range(normal_dataset.shape[0]) :
                if maximum - minimum == 0 :
                    normal_dataset[row, col] = 0.0
                else :
                    normal_dataset[row, col] = 1.0 * \
                        (maximum - normal_dataset[row, col]) / (maximum - minimum)
        return normal_dataset

    def _gzh_sorting(self) :
        """ Sort gzh by its article score and article number. """
        gzh_dict = dict()
        for article in self.article_list :
            gzh_id = article.id.split('_')[0]
            if gzh_id not in gzh_dict :
                gzh_dict[gzh_id] = []
            gzh_dict[gzh_id].append(article.score)
        gzh_list = []
        for gzh_id in gzh_dict :
            gzh_list.append([gzh_id, len(gzh_dict[gzh_id]), math.log(len(gzh_dict[gzh_id])) \
                * 1.0 * sum(gzh_dict[gzh_id]) / len(gzh_dict[gzh_id]), \
                1.0 * sum(gzh_dict[gzh_id]) / len(gzh_dict[gzh_id])])
        gzh_list = sorted(gzh_list, key=lambda x: x[2], reverse=True)
        for gzh_id, length, score, avg in gzh_list[-10:] :
            print gzh_id, length, score, avg