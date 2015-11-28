# -*- encoding = gb18030 -*-
"""
Find synonymys of the query word and can clustering word with the same topic.    

* Should use Linux Shell to run this python file.
"""

# package importing start
from synonymy.word2vector import Word2Vector
from file.path_manager import PathManager 
# package importing end


def find_synonymy(word_vector, query, synonymys) :
    from synonymy.word2vector import Word2Vector
    synonymy_searcher = Word2Vector(n_most=100, w2v_path=word_vector)
    synonymy_searcher.read_querys(query)
    synonymy_searcher.find_synonymy_words()
    synonymy_searcher.write_synonymys(synonymys)


if __name__ == '__main__' :
    word_vector = os.path.abspath(sys.argv[1])
    query = os.path.abspath(sys.argv[2])
    synonymys = os.path.abspath(sys.argv[3])
    find_synonymy(word_vector, query, synonymys)