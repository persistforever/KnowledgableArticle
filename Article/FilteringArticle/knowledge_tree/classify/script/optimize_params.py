# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from classify.run import Corpus
# package importing end


# run this script

train_article_market_path = sys.argv[1]
test_article_market_path = sys.argv[2]
pos_path = sys.argv[3]
punc_path = sys.argv[4]
klword_path = sys.argv[5]
logger_path = sys.argv[6]
corpus = Corpus()
corpus.run_optimize_params(train_article_market_path, test_article_market_path, \
        pos_path, punc_path, klword_path, logger_path)