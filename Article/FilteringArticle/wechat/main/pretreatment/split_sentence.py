# -*- encoding = gb18030 -*-
"""
Split article content into sentences.

* Should use Linux Shell to run this python file.
"""

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from pretreatment.content_to_sentence import AnotherCorpus
# package importing end


def split_sentence(article, split_char, sentence) :
    """ Split content into sub_sentence.
        Input :
            1. article_list : each line is a article, columns is [id, url, pubtime, title, ...]
        Output :
            1. sub_sentence_list : each line is a splited sentence, columns is [id, sentence].
    """

    corpus = AnotherCorpus()
    corpus.read_article_list(article)
    corpus.content_split_sentence(split_char)
    corpus.write_splited_sentence(sentence)


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    split_char = sys.argv[2].strip()
    sentence = sys.argv[3].strip()
    split_sentence(article, split_char, sentence)