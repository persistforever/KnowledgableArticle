# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from preload.run import Corpus
# package importing end


# run this script

sentences_path = sys.argv[1]
market_path = sys.argv[2]
corpus = Corpus()
corpus.run(sentences_path, market_path)