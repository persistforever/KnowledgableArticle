# -*- encoding = gb18030 -*-

# package importing start
import sys

from myunique.run import Corpus
# package importing end


# run this script

source_path = sys.argv[1]
title_path = sys.argv[2]
unique_path = sys.argv[3]
corpus = Corpus()
corpus.run(source_path, title_path, unique_path)