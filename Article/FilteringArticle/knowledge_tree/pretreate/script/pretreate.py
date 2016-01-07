# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from pretreate.run import Corpus
# package importing end


# run this script

articles_path = sys.argv[1]
participle_title_path = sys.argv[2]
treated_article_path = sys.argv[3]
corpus = Corpus()
corpus.run_pretreate(sentences_path, dictionary_path, market_path)