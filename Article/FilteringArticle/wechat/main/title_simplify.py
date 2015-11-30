# -*- encoding = gb18030 -*-
"""
Find synonymys of the query word and can clustering word with the same topic.    

* Should use Linux Shell to run this python file.
"""

# package importing start
from synonymy.word2vector import Word2Vector
from file.path_manager import PathManager 
from basic.corpus import Corpus
# package importing end


def find_synonymy(article_path, subtitle_path, keyword_path, simply_path) :
    corpus = Corpus()
    corpus.read_article_list(article_path)
    corpus.read_sub_title(subtitle_path)
    corpus.read_keyword(keyword_path)
    corpus.title_simplifying()
    corpus.write_simply_article(simply_path)


if __name__ == '__main__' :
    article = os.path.abspath(sys.argv[1])
    subtitle = os.path.abspath(sys.argv[2])
    keyword = os.path.abspath(sys.argv[3])
    simply = os.path.abspath(sys.argv[4])
    find_synonymy(article, subtitle, keyword, simply)