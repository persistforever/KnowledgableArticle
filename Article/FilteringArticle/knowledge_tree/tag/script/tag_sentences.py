# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from tag.run import Corpus
# package importing end


# run this script

tag_tree_path = sys.argv[1]
sentences_market_path = sys.argv[2]
tags_market_path = sys.argv[3]
dict_market_path = sys.argv[4]
corpus = Corpus()

corpus.run_tag_sentences(tag_tree_path, sentences_market_path, tags_market_path, dict_market_path)