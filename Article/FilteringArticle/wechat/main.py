# -*- encoding = gb18030 -*-
"""
This python file is noly used to Debug.
Can call different function to do different tasks.
If function func_name debug finished, please complete the wechat/main/func_name.py.
"""

# package importing start
# package importing end


def classifying() :
    from basic.corpus import Corpus
    from file.path_manager import PathManager
    from classifier.supervised_classifier import SvmClassifier
    corpus = Corpus()
    test_data = corpus.read_test_dataset(PathManager.CORPUS_FEATURE)
    classifier = SvmClassifier()
    classifier.sorting(test_data, corpus.article_list, clf_path=PathManager.CLASSIFIER_CLASSIFIER)
    corpus.write_knowledgeable_article(PathManager.CORPUS_KNOWLEDGE, num=10000)

def feature_select() :
    from basic.corpus import Corpus
    from file.path_manager import PathManager
    from feature.word_feature import WordExtractor
    corpus = Corpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    corpus.read_split_list(PathManager.CORPUS_SPLIT)
    corpus.feature_selecting(firpro_path=PathManager.TOOLS_FIRSTPRO, \
        secpro_path=PathManager.TOOLS_SECONDPRO, thrpro_path=PathManager.TOOLS_THIRDPRO, \
        word_path = PathManager.TOOLS_KNOWLEDGEABLEWORD, sp_path=PathManager.TOOLS_SENTENCEPST, \
        pc_path=PathManager.TOOLS_PUNCTUATION, pos_path=PathManager.TOOLS_POS)
    corpus.write_feature_list(PathManager.CORPUS_FEATURE)

def simplifying_title() :
    from file.path_manager import PathManager
    from basic.corpus import Corpus
    corpus = Corpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    corpus.read_sub_title(PathManager.CORPUS_SUBTITLE)
    corpus.read_keyword(PathManager.CORPUS_KEYWORD)
    corpus.title_simplifying(w2v_path=PathManager.CORPORA_WORD2VEC, \
        spst_path=PathManager.TOOLS_TITLESPST)
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
    lucene_list = corpus.read_lucene_list(PathManager.CORPUS_LUCENE)
    cluster = ArticleCluster(corpus_path=PathManager.CORPORA_MMCORPUS,  \
        tfidf_path=PathManager.CORPORA_TFIDF, \
        dict_path=PathManager.CORPORA_DICTIONARY, \
        w2v_path=PathManager.CORPORA_WORD2VEC, \
        lda_path=PathManager.CORPORA_LDA)
    word_dict = cluster.user_choosing(lucene_list, [u'型男<:>n'])

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
    from basic.corpora import Corpora
    from file.path_manager import PathManager
    corpus = Corpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    corpus.read_split_list(PathManager.CORPUS_SPLIT)
    texts = corpus.article_to_texts()
    corpora = Corpora()
    dictionary = corpora.create_gensim_dictionary(type='create', texts=texts, \
        path=PathManager.CORPORA_DICTIONARY)
    mmcorpus = corpora.create_gensim_corpus(type='create', texts=texts, dictionary=dictionary, \
        path=PathManager.CORPORA_MMCORPUS)
    tfidf_model = corpora.create_gensim_tfidf(type='create', mmcorpus=mmcorpus, \
        path=PathManager.CORPORA_TFIDF)
    word2tfidf = corpora.create_wordsim_tfidf(type='create', path=PathManager.CORPORA_WORD2TFIDF)
    print 'finished ...'

def create_word2vec() :
    from basic.corpus import Corpus
    from basic.corpora import Corpora
    from file.path_manager import PathManager
    corpus = Corpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    corpus.read_content_participle_sentence(PathManager.CORPUS_SENTENCE)
    sentences = corpus.article_to_sentences()
    corpora = Corpora()
    corpora.create_wordsim_word2vec(type='create', sentences=sentences, path=PathManager.CORPORA_WORD2VEC)
    print 'finished ...'

def create_lda() :
    from basic.corpus import Corpus
    from basic.corpora import Corpora
    from file.path_manager import PathManager
    corpus = Corpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    corpus.read_split_list(PathManager.CORPUS_SPLIT)
    texts = corpus.article_to_texts()
    corpora = Corpora()
    dictionary = corpora.create_gensim_dictionary(type='create', texts=texts, \
        path=PathManager.CORPORA_DICTIONARY)
    mmcorpus = corpora.create_gensim_corpus(type='create', texts=texts, dictionary=dictionary, \
        path=PathManager.CORPORA_MMCORPUS)
    corpora.create_lda_model(type='create', mmcorpus=mmcorpus, dictionary=dictionary, \
        path=PathManager.CORPORA_LDA)
    print 'finished ...'

def filter_word() :
    from basic.corpus import Corpus
    from file.path_manager import PathManager
    corpus = Corpus()
    wordbag = corpus.read_wordbag(PathManager.BOWS_IDF, sp_char=':')
    wordbag = corpus.filter_word(wordbag, topn=10000)
    corpus.write_wordbag(wordbag, PathManager.BOWS_WORD)
    print 'finished ...'

def create_classifier() :
    from basic.corpus import Corpus
    from file.path_manager import PathManager
    from classifier.supervised_classifier import SvmClassifier
    corpus = Corpus()
    corpus.read_train_dataset(train_path=PathManager.CORPUS_TRAINDATA)
    classifier = SvmClassifier()
    clf = classifier.training(corpus.train_dataset, corpus.train_label)
    classifier.storing(clf, path=PathManager.CLASSIFIER_CLASSIFIER)
    
def content_split_sentence() :
    from basic.corpus import Corpus
    from file.path_manager import PathManager
    from pretreatment.content_to_sentence import AnotherCorpus
    corpus = AnotherCorpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    corpus.content_split_sentence(PathManager.TOOLS_SENTENCEPST)
    corpus.write_content_sentence_list(PathManager.CORPUS_SENTENCE)

def simplifying_content() :
    from basic.corpus import Corpus
    from file.path_manager import PathManager
    from simplifier.content_simplifier import AnotherCorpus
    corpus = AnotherCorpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    corpus.read_content_sentence_list(PathManager.CORPUS_SENTENCE)
    corpus.simplify_content(rd_path=PathManager.TOOLS_REDUNDANCE)
    corpus.write_article_list(length=100, article_path=PathManager.CORPUS_SIMPLYARTICLE)
 
def word_cluster() :
    from file.path_manager import PathManager
    from basic.corpus import Corpus
    from cluster.word_cluster import WordCluster
    from cluster.lda_cluster import LdaCluster
    corpus = Corpus()
    corpus.read_article_list(PathManager.CORPUS_ARTICLE)
    cluster = WordCluster(corpus_path=PathManager.CORPORA_MMCORPUS,  \
        tfidf_path=PathManager.CORPORA_TFIDF, \
        dict_path=PathManager.CORPORA_DICTIONARY, \
        w2v_path=PathManager.CORPORA_WORD2VEC, \
        lda_path=PathManager.CORPORA_LDA)
    cluster.read_test_label(data_path=PathManager.CLUSTER_TESTDATA)
    doc_topic_, topic_word_ = cluster.process(corpus.article_list)
    cluster.write_article_topic(doc_topic_, label_path=PathManager.CLUSTER_DOCTOPIC)
    cluster.write_article_topic(topic_word_, label_path=PathManager.CLUSTER_TOPICWORD)
    print 'finish'


if __name__ == '__main__' :
    # 5classifying()
    # simplifying_title()
    # simplifying_article()
    # tagging_article()
    # qa_system()
    # create_corpora()
    # create_word2vec()\
    # create_lda()
    create_article_info()
    # find_synonymy()
    # filter_word()
    # feature_select()
    # create_classifier()
    # content_split_sentence()
    # simplifying_content()
    # word_cluster()