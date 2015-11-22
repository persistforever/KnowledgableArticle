# -*- encoding = gb18030 -*-
"""
Main entry of the project
    first step: filtering knowledgeable article.
"""
from basic.corpus import Corpus


def classifying() :
    corpus = Corpus()
    corpus.read_train_dataset()
    corpus.read_article_list()
    corpus.read_test_dataset()
    #sortedlist = corpus.classifying(2)
    #corpus.writeKnowledgableArticle(filepath.getOutputKnowledgablearticle(type, date), sortedlist, rate=0.2)


if __name__ == '__main__' :
    classifying()