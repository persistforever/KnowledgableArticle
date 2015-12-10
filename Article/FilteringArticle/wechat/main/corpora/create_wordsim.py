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

from basic.corpora import Corpora
# package importing end


def create_corpora(dictionary_path, mmcorpu_path, tfidf_path, wordsim_path) :
    corpora = Corpora()
    dictionary = corpora.create_gensim_dictionary(type='load', path=dictionary_path)
    mmcorpus = corpora.create_gensim_corpus(type='load', path=mmcorpu_path)
    tfidf_model = corpora.create_gensim_tfidf(type='load', path=tfidf_path)
    word2tfidf = corpora.create_wordsim_tfidf(type='create', mmcorpus=mmcorpus, dictionary=dictionary, \
        tfidf_model=tfidf_model, path=wordsim_path)


if __name__ == '__main__' :
    dictionary = sys.argv[1].strip()
    mmcorpus = sys.argv[2].strip()
    tfidf_model = sys.argv[3].strip()
    word_sim = sys.argv[4].strip()
    create_corpora(dictionary, mmcorpus, tfidf_model, word_sim)