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


def create_corpora(artice_path, split_path, dictionary_path, mmcorpu_path, tfidf_path) :
    corpus = Corpus()
    corpus.read_article_list(artice_path)
    corpus.read_split_list(split_path)
    texts = corpus.article_to_texts()
    corpora = Corpora()
    dictionary = corpora.create_gensim_dictionary(type='create', texts=texts, \
        path=dictionary_path)
    mmcorpus = corpora.create_gensim_corpus(type='create', texts=texts, dictionary=dictionary, \
        path=mmcorpu_path)
    tfidf_model = corpora.create_gensim_tfidf(type='create', mmcorpus=mmcorpus, \
        path=tfidf_path)


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    split = sys.argv[2].strip()
    dictionary = sys.argv[3].strip()
    mmcorpus = sys.argv[4].strip()
    tfidf_model = sys.argv[5].strip()
    create_corpora(article, split, dictionary, mmcorpus, tfidf_model)