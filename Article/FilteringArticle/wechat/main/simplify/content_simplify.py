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
from simplifier.content_simplifier import AnotherCorpus
# package importing end


def content_simplify(article, sentence, redundance, simply) :
    corpus = AnotherCorpus()
    corpus.read_article_list(article)
    corpus.read_content_sentence_list(sentence)
    corpus.simplify_content(rd_path=redundance)
    corpus.write_article_list(length=100, article_path=simply)


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    sentence = sys.argv[2].strip()
    redundance = sys.argv[3].strip()
    simply = sys.argv[4].strip()
    content_simplify(article, sentence, redundance, simply)