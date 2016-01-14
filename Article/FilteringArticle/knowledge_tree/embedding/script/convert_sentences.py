# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from embedding.run import Corpus
# package importing end


# run this script

sentences_path = sys.argv[1]
sentences_market_path = sys.argv[2]
corpus = Corpus()
corpus.run_convert_sentences(sentences_path, sentences_market_path)