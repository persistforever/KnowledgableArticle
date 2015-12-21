﻿# -*- encoding = gb18030 -*-
"""
Find synonymys of the query word and can clustering word with the same topic.    

* Should use Linux Shell to run this python file.
"""

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from basic.corpus import Corpus
from simplifier.segementor import ContentSegementor
# package importing end


def segemented_content(article, sentence, sentence_spst) :
    corpus = Corpus()
    corpus.article_info(article, type='load')
    segementor = ContentSegementor(sentence_spst)
    corpus.segemented_list(sentence, type='create', target='content', \
        segementor=segementor)

if __name__ == '__main__' :
    article = sys.argv[1].strip()
    sentence = sys.argv[2].strip()
    sentence_spst = sys.argv[3].strip()
    segemented_content(article, sentence, sentence_spst)