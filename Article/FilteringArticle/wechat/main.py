# -*- encoding = gb18030 -*-
"""
Main entry of the project
    first step: filtering knowledgeable article.
"""
from basic.corpus import Corpus
from tag.word_bag import WordBag


def classifying() :
    corpus = Corpus()
    corpus.read_train_dataset()
    corpus.read_article_list()
    corpus.read_test_dataset()
    corpus.classifying(2)
    corpus.write_knowledgeable_article(rate=0.2)

def simplifying_article() :
    wordbag = WordBag()
    wordbag.get_word_bag()


if __name__ == '__main__' :
    # classifying()
    simplifying_article()