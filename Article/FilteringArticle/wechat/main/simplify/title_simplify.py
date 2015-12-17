# -*- encoding = gb18030 -*-
"""
Find synonymys of the query word and can clustering word with the same topic.    

* Should use Linux Shell to run this python file.
"""

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from basic.corpus import Corpus
from basic.corpora import Corpora
from simplifier.simplifier import TitleSimplifier
# package importing end


def simplifying_title(article, subtitle, dictionary, texts, \
    tfidf, word2vec, simply) :
    corpus = Corpus()
    corpus.article_info(article, type='load')
    corpus.segemented_participle_list(subtitle, type='load', target='title')
    corpora = Corpora()
    dictionary = corpora.word_dictionary(type='load', path=dictionary)
    texts = corpora.article_texts_bow(type='load', path=texts)
    tfidf = corpora.textsbow_to_tfidf(type='load', path=tfidf)
    simplifier = TitleSimplifier(word2vec_path=word2vec)
    corpus.simplify_title(dictionary, texts, tfidf, simplifier=simplifier)
    corpus.article_info(simply, type='create')


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    subtitle = sys.argv[2].strip()
    dictionary = sys.argv[3].strip()
    texts = sys.argv[4].strip()
    tfidf = sys.argv[5].strip()
    word2vec = sys.argv[6].strip()
    simply = sys.argv[7].strip()
    simplifying_title(article, subtitle, dictionary, texts, tfidf, word2vec, simply)