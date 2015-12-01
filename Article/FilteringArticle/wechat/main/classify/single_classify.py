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


def classify(article_path, knowledge_path, number) :
    corpus = Corpus()
    corpus.read_article_list(article_path)
    corpus.classifying('single_condition')
    corpus.write_knowledgeable_article(knowledge_path, num=int(number))


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    knowledge = sys.argv[2].strip()
    number = sys.argv[3].strip()
    classify(article, knowledge, number)