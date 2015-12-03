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
from feature.word_feature import NarrativeExtractor
# package importing end


def extract(article_path, split_path, firpro_path, secpro_path, thrpro_path, \
    feature_path) :
    corpus = Corpus()
    corpus.read_article_list(article_path)
    corpus.read_split_list(split_path)
    selector = NarrativeExtractor(firpro_path=firpro_path, secpro_path=secpro_path, \
        thrpro_path=thrpro_path)
    selector.extractFeature(corpus.article_list)
    corpus.write_feature_list(feature_path)


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    split = sys.argv[2].strip()
    firpro = sys.argv[3].strip()
    secpro = sys.argv[4].strip()
    thrpro = sys.argv[5].strip()
    feature = sys.argv[6].strip()
    extract(article, split, firpro, secpro, thrpro, feature)