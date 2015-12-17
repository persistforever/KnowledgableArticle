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


def create_dictionary(artice_path, title_split_path, content_split_path, \
    dictionary_path) :
    corpus = Corpus()
    corpus.article_info(artice_path, type='load')
    corpus.participle_list(title_split_path, type='load', target='participle_title')
    corpus.participle_list(content_split_path, type='load', target='participle_content')
    texts = corpus.article_to_texts(target='participle_title')
    texts.extend(corpus.article_to_texts(target='participle_content'))
    corpora = Corpora()
    dictionary = corpora.word_dictionary(type='create', texts=texts, \
        path=dictionary_path)


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    title_split = sys.argv[2].strip()
    content_split = sys.argv[3].strip()
    dictionary = sys.argv[4].strip()
    create_dictionary(article, title_split, content_split, dictionary)