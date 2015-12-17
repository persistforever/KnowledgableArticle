# -*- encoding = gb18030 -*-
"""
Create some file in copora.
By using some APIs in gensim.

* Should use Linux Shell to run this python file.
"""

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from basic.corpus import Corpus
from basic.corpora import Corpora
# package importing end


def create_word_vector(article_path, sentence_path, w2v_path) :
    corpus = Corpus()
    corpus.article_info(article_path, type='load')
    corpus.segemented_participle_list(sentence_path, type='load', target='content')
    sentences = corpus.article_to_sentences(target='segemented_participle_content')
    corpora = Corpora()
    corpora.word_to_vector(type='create', sentences=sentences, path=w2v_path)


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    sentence = sys.argv[2].strip()
    word2vec = sys.argv[3].strip()
    create_word_vector(article, sentence, word2vec)