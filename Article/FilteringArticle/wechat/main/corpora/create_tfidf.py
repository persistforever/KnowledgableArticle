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


def create_corpora(texts_path, tfidf_path) :
    corpora = Corpora()
    texts = corpora.article_texts_bow(type='load', path=texts_path)
    tfidf = corpora.textsbow_to_tfidf(type='create', textsbow=texts, path=tfidf_path)


if __name__ == '__main__' :
    texts = sys.argv[1].strip()
    tfidf = sys.argv[2].strip()
    create_corpora(texts, tfidf)