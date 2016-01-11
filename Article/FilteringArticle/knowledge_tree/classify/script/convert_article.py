# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from classify.run import Corpus
# package importing end


# run this script

articles_path = sys.argv[1]
article_market_path = sys.argv[2]
corpus = Corpus()
corpus.run_convert_article(articles_path, article_market_path)