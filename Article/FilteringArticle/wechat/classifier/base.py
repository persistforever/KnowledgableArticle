# -*- encoding = gb18030 -*-
""" Basic class of Classifier """


class BaseClassifier :

    def sorting(self, article_list) :
        """ Sort article list and return sorted article list. """

    def set_training_set(self, train_data, train_label) :
        """ Set the training set of the classifier. """
        self.train_data = train_data
        self.train_label = train_label