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


def create_corpora(mmcorpu_path, tfidf_path) :
    corpora = Corpora()
    mmcorpus = corpora.create_gensim_corpus(type='load', path=mmcorpu_path)
    tfidf_model = corpora.create_gensim_tfidf(type='create', mmcorpus=mmcorpus, \
        path=tfidf_path)


if __name__ == '__main__' :
    mmcorpus = sys.argv[1].strip()
    tfidf_model = sys.argv[2].strip()
    create_corpora(mmcorpus, tfidf_model)