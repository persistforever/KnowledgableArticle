# -*- encoding = gb18030 -*-
"""
Find synonymys of the query word and can clustering word with the same topic.    

* Should use Linux Shell to run this python file.
"""

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from basic.corpus import Corpus
from simplifier.simplifier import ContentSimplifier
# package importing end


def simplifying_content(article, sentence, redundance, simply) :
    corpus = Corpus()
    corpus = Corpus()
    corpus.article_info(article)
    corpus.segemented_list(sentence, type='load', target='content')
    simplifier = ContentSimplifier(redundance)
    corpus.simplify_content(target='content', simplifier=simplifier)
    corpus.article_info(simply, type='create')


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    sentence = sys.argv[2].strip()
    redundance = sys.argv[3].strip()
    simply = sys.argv[4].strip()
    simplifying_content(article, sentence, redundance, simply)