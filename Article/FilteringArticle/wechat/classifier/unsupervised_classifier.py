# -*- encoding = gb18030 -*-
""" unsupervised classifier 
    1. MultiConditionClassifier 
"""
from base import BaseClassifier


class MultiConditionClassifier(BaseClassifier) :

    def sorting(self, article_list) :
        """ Sort the article list within multiple condition. """
        sorted_article_list = sorted(article_list, key=lambda article: ( \
            article.feature_set[21], article.feature_set[23], \
            article.feature_set[25], article.feature_set[27], \
            -article.feature_set[15], -article.feature_set[13], \
            -article.feature_set[1]), reverse=True)
        return sorted_article_list


class SingleConditionClassifier(BaseClassifier) :

    def __init__(self) :
        pass
    
    def sorting(self, article_list) :
        """ Sort the article list within single condition. """
        sorted_article_list = sorted(article_list, \
            key=lambda article: float(article.featured), reverse=True)
        return sorted_article_list