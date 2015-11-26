# -*- encoding = gb18030 -*-
"""
Main entry of the project
    first step: filtering knowledgeable article.
"""
from basic.corpus import Corpus
from basic.word import Word
from tag.word_bag import WordBag
from tag.tag_article import Tagger
from qa.article_tag import ArticleCluster


def classifying() :
    corpus = Corpus()
    corpus.read_train_dataset()
    corpus.read_article_list()
    corpus.read_test_dataset()
    corpus.classifying(2)
    corpus.write_knowledgeable_article(rate=0.2)

def simplifying_title() :
    corpus = Corpus()
    corpus.read_knowledgeable()
    corpus.read_sub_title()
    corpus.read_keyword()
    corpus.title_simplifying()
    corpus.write_simply_knowledgeable_article()

def simplifying_article() :
    corpus = Corpus()
    corpus.read_article_list()
    wordbag = WordBag()
    # wordbag.get_word_bag()
    wordbag.observe_lda()

def tagging_article() :
    tagger = Tagger()
    tagger.read_tag_list()
    corpus = Corpus()
    corpus.read_keyword()
    print len(corpus.article_list)
    tagger.tag_article_list(corpus.article_list)
    corpus.write_tag_list()

def qa_system() :
    corpus = Corpus()
    corpus.read_qa_article()
    corpus.read_keyword()
    corpus.read_sub_sentence()
    cluster = ArticleCluster()
    cluster.article_clustering(corpus.article_list, [u'扎', u'头发'])


if __name__ == '__main__' :
    # classifying()
    # simplifying_title()
    # simplifying_article()
    # tagging_article()
    qa_system()