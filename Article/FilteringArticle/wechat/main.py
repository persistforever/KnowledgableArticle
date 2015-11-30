# -*- encoding = gb18030 -*-
"""
This python file is noly used to Debug.
Can call different function to do different tasks.
If function func_name debug finished, please complete the wechat/main/func_name.py.
"""

# package importing start
# package importing end


def classifying() :
    corpus = Corpus()
    corpus.read_train_dataset()
    corpus.read_article_list()
    corpus.read_test_dataset()
    corpus.classifying(2)
    corpus.write_knowledgeable_article(rate=0.2)

def simplifying_title() :
    from file.path_manager import PathManager
    from basic.corpus import Corpus
    corpus = Corpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    corpus.read_sub_title(PathManager.CORPUS_SUBTITLE)
    corpus.read_keyword(PathManager.CORPUS_KEYWORD)
    corpus.title_simplifying()
    corpus.write_simply_article(PathManager.CORPUS_SIMPLYARTICLE)

def simplifying_article() :
    corpus = Corpus()
    corpus.read_article_list()
    wordbag = WordBag()
    # wordbag.get_word_bag()
    wordbag.observe_lda()

def tagging_article() :
    tagger = Tagger()
    tagger.read_tag_list()
    corpus = Corpus()
    corpus.read_keyword()
    print len(corpus.article_list)
    tagger.tag_article_list(corpus.article_list)
    corpus.write_tag_list()

def qa_system() :
    from file.path_manager import PathManager
    from basic.corpus import Corpus
    from qa.article_tag import ArticleCluster
    corpus = Corpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    cluster = ArticleCluster(corpus_path=PathManager.CORPORA_MMCORPUS,  \
        tfidf_path=PathManager.CORPORA_TFIDF, \
        dict_path=PathManager.CORPORA_DICTIONARY, \
        w2v_path=PathManager.CORPORA_WORD2VEC)
    word_dict = cluster.article_tfidf(corpus.article_list, [u'瑜伽<:>nz'])
    cluster.word_clustering(word_dict)
    # cluster.article_clustering(corpus.article_list, [u'瑜伽<:>nz'])

def find_synonymy() :
    from file.path_manager import PathManager
    from synonymy.word2vector import Word2Vector
    # from synonymy.bagofword import BagOfWord
    # synonymy_searcher = BagOfWord(n_most=100, w2t_path=PathManager.CORPORA_WORD2TFIDF, \
    #     dict_path=PathManager.CORPORA_DICTIONARY)
    synonymy_searcher = Word2Vector(n_most=100, w2v_path=PathManager.CORPORA_WORD2VEC)
    synonymy_searcher.read_querys(PathManager.SYNONYMYS_QUERY)
    synonymy_searcher.find_synonymy_words()
    synonymy_searcher.write_synonymys(PathManager.SYNONYMYS_SYNONYMY)

def create_corpora() :
    from basic.corpus import Corpus
    from file.path_manager import PathManager
    corpus = Corpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    corpus.read_split_list(PathManager.CORPUS_SPLIT)
    wordbag = corpus.read_wordbag(PathManager.BOWS_WORD, sp_char='<:>')
    texts = corpus.article_to_texts()
    tokens = corpus.word_to_tokens(wordbag)
    dictionary = corpus.create_gensim_dictionary(type='init', texts=texts, tokens=tokens, \
        path=PathManager.CORPORA_DICTIONARY)
    mmcorpus = corpus.create_gensim_corpus(type='init', texts=texts, dictionary=dictionary, \
        path=PathManager.CORPORA_MMCORPUS)
    tfidf_model = corpus.create_gensim_tfidf(type='init', mmcorpus=mmcorpus, \
        path=PathManager.CORPORA_TFIDF)
    word2tfidf = corpus.create_wordsim_tfidf(type='init', mmcorpus=mmcorpus, dictionary=dictionary, \
        tfidf_model=tfidf_model, path=PathManager.CORPORA_WORD2TFIDF)
    print 'finished ...'

def create_word2vec() :
    from basic.corpus import Corpus
    from file.path_manager import PathManager
    corpus = Corpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    corpus.read_sentence_list(PathManager.CORPUS_SENTENCE)
    sentences = corpus.article_to_sentences()
    corpus.create_wordsim_word2vec(type='init', sentences=sentences, path=PathManager.CORPORA_WORD2VEC)
    print 'finished ...'

def filter_word() :
    from basic.corpus import Corpus
    from file.path_manager import PathManager
    corpus = Corpus()
    wordbag = corpus.read_wordbag(PathManager.BOWS_IDF, sp_char=':')
    wordbag = corpus.filter_word(wordbag, topn=10000)
    corpus.write_wordbag(wordbag, PathManager.BOWS_WORD)
    print 'finished ...'


if __name__ == '__main__' :
    # classifying()
    simplifying_title()
    # simplifying_article()
    # tagging_article()
    # qa_system()
    # create_corpora()
    # create_word2vec()
    # find_synonymy()
    # filter_word()