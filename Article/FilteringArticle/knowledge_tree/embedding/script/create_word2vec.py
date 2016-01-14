# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from embedding.run import Corpus
# package importing end


# run this script

sentences_path = sys.argv[1]
word_embedding_path = sys.argv[2]
word_embedding_market_path = sys.argv[3]
corpus = Corpus()
corpus.run_create_word2vec(sentences_path, word_embedding_path, word_embedding_market_path)