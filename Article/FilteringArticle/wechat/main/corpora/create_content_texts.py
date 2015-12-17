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


def create_content_texts(artice_path, split_path, dictionary_path, texts_path) :
    corpus = Corpus()
    corpus.article_info(artice_path, type='load')
    corpus.participle_list(split_path, type='load', target='participle_content')
    texts = corpus.article_to_texts(target='participle_content')
    corpora = Corpora()
    dictionary = corpora.word_dictionary(type='load', path=dictionary_path)
    mmcorpus = corpora.article_texts_bow(type='create', texts=texts, dictionary=dictionary, \
        path=texts_path)


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    split = sys.argv[2].strip()
    dictionary = sys.argv[3].strip()
    texts = sys.argv[4].strip()
    create_content_texts(article, split, dictionary, texts)