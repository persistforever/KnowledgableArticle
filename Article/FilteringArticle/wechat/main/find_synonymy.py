# -*- encoding = gb18030 -*-
"""
Main entry of the project
    first step: filtering knowledgeable article.
"""

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from synonymy.word2vector import Word2Vector
# package importing end


def find_synonymy(word_vector, query, synonymys) :
    synonymy_searcher = Word2Vector(n_most=100, w2v_path=word_vector)
    synonymy_searcher.read_querys(query)
    synonymy_searcher.find_synonymy_words()
    synonymy_searcher.write_synonymys(synonymys)


if __name__ == '__main__' :
    # word_vector = os.path.abspath('E://file/knowledge/tools/word2vector/fashion_vectors.txt')
    # query = os.path.abspath('E://file/knowledge/synonymys/query')
    # synonymys = os.path.abspath('E://file/knowledge/synonymys/synonymy')
    word_vector = os.path.abspath(sys.argv[1])
    query = os.path.abspath(sys.argv[2])
    synonymys = os.path.abspath(sys.argv[3])
    find_synonymy(word_vector, query, synonymys)