# -*- encoding = gb18030 -*-
"""
This python file is noly used to Debug.
Can call different function to do different tasks.
If function func_name debug finished, please complete the wechat/main/func_name.py.
"""

# package importing start
import os
import sys

from basic.corpus import Corpus
from basic.word import Word
from tag.word_bag import WordBag
from tag.tag_article import Tagger
from qa.article_tag import ArticleCluster
from file.path_manager import PathManager
# package importing end


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
    # corpus.read_sub_sentence()
    cluster = ArticleCluster()
    cluster.article_clustering(corpus.article_list, [u'男装'])

def find_synonymy() :
    from synonymy.bagofword import BagOfWord
    synonymy_searcher = BagOfWord(n_most=100, bow_path=PathManager.BOWS_BOW)
    synonymy_searcher.read_word(word_path=PathManager.BOWS_WORD)
    # synonymy_searcher.read_querys(PathManager.SYNONYMYS_QUERY)
    # synonymy_searcher.find_synonymy_words()
    # synonymy_searcher.write_synonymys(PathManager.SYNONYMYS_SYNONYMY)

def create_corpora() :
    from basic.corpus import Corpus
    from file.path_manager import PathManager
    corpus = Corpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    corpus.read_split_list(PathManager.CORPUS_SPLIT)
    corpus.read_wordbag(PathManager.BOWS_WORD)
    texts = corpus.article_to_texts()
    tokens = corpus.word_to_tokens()
    dictionary = corpus.create_gensim_dictionary(type='load', path=PathManager.CORPORA_DICTIONARY)
    # dictionary = corpus.create_gensim_dictionary(type='init', texts=texts, tokens=tokens)
    # dictionary.save(PathManager.CORPORA_DICTIONARY)


if __name__ == '__main__' :
    # classifying()
    # simplifying_title()
    # simplifying_article()
    # tagging_article()
    # qa_system()
    # find_synonymy()
    create_corpora()