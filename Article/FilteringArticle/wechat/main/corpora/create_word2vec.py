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


def create_corpora(artice_path, sentence_path, w2v_path) :
    corpus = Corpus()
    corpus.read_article_list(artice_path)
    corpus.read_sub_sentence_list(sentence_path)
    sentences = corpus.article_to_sentences()
    corpus.create_wordsim_word2vec(type='init', sentences=sentences, path=w2v_path)
    print 'finished ...'


if __name__ == '__main__' :
    article = sys.argv[1].strip()
    sentence = sys.argv[2].strip()
    word2vec = sys.argv[3].strip()
    create_corpora(article, sentence, word2vec)