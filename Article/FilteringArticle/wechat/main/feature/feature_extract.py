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


def extract(article_path, split_path, firpro_path, secpro_path, thrpro_path, \
    word_path, sp_path, pc_path, pos_path, feature_path) :
    corpus = Corpus()
    corpus.read_article_list(article_path)
    corpus.read_split_list(split_path)
    corpus.feature_selecting(firpro_path=firpro_path, secpro_path=secpro_path, \
        thrpro_path=thrpro_path, word_path=word_path, sp_path=sp_path, \
        pc_path=pc_path, pos_path=pos_path)
    corpus.write_feature_list(feature_path)


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    split = sys.argv[2].strip()
    firpro = sys.argv[3].strip()
    secpro = sys.argv[4].strip()
    thrpro = sys.argv[5].strip()
    word = sys.argv[6].strip()
    sp = sys.argv[7].strip()
    pc = sys.argv[8].strip()
    pos = sys.argv[9].strip()
    feature = sys.argv[10].strip()
    extract(article, split, firpro, secpro, thrpro, word, sp, pc, pos, feature)