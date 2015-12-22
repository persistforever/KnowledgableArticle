# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from word.run import Corpus
# package importing end


# run this script

sentences_path = sys.argv[1]
dictionary_path = sys.argv[2]
corpus = Corpus()
corpus.run_create_dictionary(sentences_path, \
        dictionary_path)