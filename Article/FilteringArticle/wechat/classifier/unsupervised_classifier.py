# -*- encoding = gb18030 -*-
""" Basic class of Classifier """
from base import BaseClassifier


class MultiConditionClassifier(BaseClassifier) :

    def classifying(self, article_list) :
        """ Sort the article list within multiple condition. """
        sortedlist = sorted(article_list, key=lambda x: ( \
            x.featureset[21], x.featureset[23], x.featureset[25], x.featureset[27], \
            -x.featureset[15], -x.featureset[13], -x.featureset[1]), reverse=True)
        return sorted_article_list