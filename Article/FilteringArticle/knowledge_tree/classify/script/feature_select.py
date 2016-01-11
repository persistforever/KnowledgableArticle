# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from classify.run import Corpus
# package importing end


# run this script

article_market_path = sys.argv[1]
feature_path = sys.argv[2]
feature_market_path = sys.argv[3]
pos_path = sys.argv[4]
punc_path = sys.argv[5]
klword_path = sys.argv[6]
corpus = Corpus()
corpus.run_feature_select(article_market_path, pos_path, punc_path, klword_path, \
        feature_path, feature_market_path)