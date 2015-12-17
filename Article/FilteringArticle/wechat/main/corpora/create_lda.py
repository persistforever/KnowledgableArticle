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


def create_lda(dictionary_path, mmcorpu_path, tfidf_path, lda_model, num) :
    corpora = Corpora()
    dictionary = corpora.word_dictionary(type='load', path=dictionary_path)
    mmcorpus = corpora.create_gensim_corpus(type='load', path=mmcorpu_path)
    tfidf_model = corpora.create_gensim_tfidf(type='load', path=tfidf_path)
    corpora.create_lda_model(type='create', mmcorpus=mmcorpus, dictionary=dictionary, \
        path=lda_model, n_topics=int(num))


if __name__ == '__main__' :
    dictionary = sys.argv[1].strip()
    mmcorpus = sys.argv[2].strip()
    tfidf_model = sys.argv[3].strip()
    lda_model = sys.argv[4].strip()
    num = sys.argv[5].strip()
    create_lda(dictionary, mmcorpus, tfidf_model, lda_model, num)