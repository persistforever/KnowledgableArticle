# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from tag.run import Corpus
# package importing end


# run this script

sentences_path = sys.argv[1]
tag_tree_path = sys.argv[2]
tags_path = sys.argv[3]
sentences_market_path = sys.argv[4]
tags_market_path = sys.argv[5]
untag_sentence_path = sys.argv[6]
func = sys.argv[7]
corpus = Corpus()

if func == 'run_convert_sentences' :
    corpus.run_convert_sentences(sentences_path, sentences_market_path)   
elif func == 'run_tag_sentences' :
    corpus.run_tag_sentences(tag_tree_path, sentences_market_path, tags_path, \
        tags_market_path, untag_sentence_path)