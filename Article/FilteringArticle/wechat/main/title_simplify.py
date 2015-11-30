# -*- encoding = gb18030 -*-
"""
Find synonymys of the query word and can clustering word with the same topic.    

* Should use Linux Shell to run this python file.
"""

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from basic.corpus import Corpus
# package importing end


def find_synonymy(article_path, subtitle_path, keyword_path, simply_path, \
    w2v_path, spst_path) :
    corpus = Corpus()
    corpus.read_article_list(article_path)
    corpus.read_sub_title(subtitle_path)
    corpus.read_keyword(keyword_path)
    corpus.title_simplifying(w2v_path=w2v_path, spst_path=spst_path)
    corpus.write_simply_article(simply_path)


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    subtitle = sys.argv[2].strip()
    keyword = sys.argv[3].strip()
    simply = sys.argv[4].strip()
    word2vec = sys.argv[5].strip()
    titlespst = sys.argv[6].strip()
    find_synonymy(article, subtitle, keyword, simply, word2vec, titlespst)