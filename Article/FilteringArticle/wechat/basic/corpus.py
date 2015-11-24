# -*- encoding = gb18030 -*-
""" Class corpus """
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import numpy as np
from article import Article
from file.file_operator import BaseFileOperator, CSVFileOperator, TextFileOperator
from file.path_manager import PathManager
from classifier.unsupervised_classifier import MultiConditionClassifier
from classifier.supervised_classifier import SvmClassifier


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
        data_list = self.file_operator.reading(self.path_manager.get_output_article())
        for data in data_list :
            article = Article()
            if len(data) >= 4 :
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
        data_list = self.file_operator.reading(self.path_manager.get_input_traindataset())
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
        data_list = self.file_operator.reading(self.path_manager.get_output_testdataset())
        test_dataset = np.array([np.array(line[1:]) for line in data_list], dtype=float)
        self.test_dataset = self._normalization(test_dataset)
        for idx in range(len(data_list)) :
            id = data_list[idx][0]
            if id in self._id_article :
                self._id_article[id].import_feature_set(list(self.test_dataset[idx]))
        print 'reading test dataset finished ...'

    def read_keyword(self) :
        """ Read key_word from input/keyword.
        Each row of the file is a article.
        column[0] of the file is the id of the article.
        Each column[1:] of the file is the keyword of the article. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_output_keyword())
        for data in data_list :
            article = Article()
            article.set_params(id=data[0])
            article.import_keyword(data, length=100)
            self.article_list.append(article)
        print 'reading keyword finished ...'
        self._constr_dict_id()
    
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
        print 'classifying article_list finished ...'

    def write_knowledgeable_article(self, rate=0.1) :
        """ Write knowledgeable article into output/knowledgeable.
        Each row of file is article.
        Each column of file is the attributes of the article. """
        self.file_operator = CSVFileOperator()
        length = int(len(self.sorted_article_list) * rate)
        data_list = []
        for article in self.sorted_article_list[0:length] :
            data_list.append(article.get_article())
        self.file_operator.writing(data_list, self.path_manager.get_output_knowledgable())
        print 'wrirting knowledgeable article finished ...'

    def write_tag_list(self) :
        """ Write tag list of article.
        Each row of file is an article.
        Each column of file is the tags of the article. """
        self.file_operator = CSVFileOperator()
        data_list = []
        for article in self.article_list :
            data_list.append(article.get_tag_list())
        self.file_operator.writing(data_list, self.path_manager.get_output_article_tag())
        print 'wrirting article tag_list finished ...'

    def _constr_dict_id(self) :
        """ Construct id_article dict.
        key is id, value is Article object. """
        self._id_article = dict()
        for article in self.article_list :
            if article.id not in self._id_article :
                self._id_article[article.id] = article
        print 'constructing _id_article dict finished ...'

    def _normalization(self, dataset) :
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