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
# package importing end


def create_corpora(artice_path, split_path, wordbag_path, \
    dictionary_path, mmcorpu_path, tfidf_path) :
    corpus = Corpus()
    corpus.read_article_list(artice_path)
    corpus.read_split_list(split_path)
    wordbag = corpus.read_wordbag(wordbag_path, sp_char='<:>')
    texts = corpus.article_to_texts()
    tokens = corpus.word_to_tokens(wordbag)
    dictionary = corpus.create_gensim_dictionary(type='init', texts=texts, tokens=tokens, \
        path=dictionary_path)
    mmcorpus = corpus.create_gensim_corpus(type='init', texts=texts, dictionary=dictionary, \
        path=mmcorpu_path)
    tfidf_model = corpus.create_gensim_tfidf(type='init', mmcorpus=mmcorpus, \
        path=tfidf_path)


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    split = sys.argv[2].strip()
    wordbag = sys.argv[3].strip()
    dictionary = sys.argv[4].strip()
    mmcorpus = sys.argv[5].strip()
    tfidf_model = sys.argv[6].strip()
    create_corpora(article, split, wordbag, dictionary, mmcorpus, tfidf_model)