# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from segment.run import Corpus
# package importing end


# run this script

source_path = sys.argv[1]
title_spst_path = sys.argv[2]
content_spst_path = sys.argv[3]
sentence_path = sys.argv[4]
seg_title_path = sys.argv[5]
seg_content_path = sys.argv[6]
corpus = Corpus()
corpus.run(source_path, title_spst_path, content_spst_path, \
        sentence_path, seg_title_path, seg_content_path)