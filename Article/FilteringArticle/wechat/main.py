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

def create_texts() :
    from basic.corpus import Corpus
    from basic.corpora import Corpora
    from file.path_manager import PathManager
    corpus = Corpus()
    corpus.article_info(PathManager.CORPUS_ARTICLE, type='load')
    corpus.participle_list(PathManager.CORPUS_SPLIT, \
        type='load', target='participle_title')
    texts = corpus.article_to_texts(target='participle_title')
    corpora = Corpora()
    dictionary = corpora.word_dictionary(type='load', texts=texts, \
        path=PathManager.CORPORA_DICTIONARY)
    texts = corpora.article_texts_bow(type='load', texts=texts, dictionary=dictionary, \
        path=PathManager.CORPORA_TITLETEXTS)
    print 'finished ...'

def create_tfidf() :
    from basic.corpus import Corpus
    from basic.corpora import Corpora
    from file.path_manager import PathManager
    corpora = Corpora()
    dictionary = corpora.word_dictionary(type='load', path=PathManager.CORPORA_DICTIONARY)
    texts = corpora.article_texts_bow(type='load', path=PathManager.CORPORA_CONTENTTEXTS)
    tfidf = corpora.textsbow_to_tfidf(type='create', textsbow=texts, path=PathManager.CORPORA_TFIDF)
    print 'finished ...'

def create_word2vec() :
    from basic.corpus import Corpus
    from basic.corpora import Corpora
    from file.path_manager import PathManager
    corpus = Corpus()
    corpus.article_info(PathManager.CORPUS_SIMPLYARTICLE, type='load')
    corpus.segemented_participle_list(PathManager.CORPUS_SENTENCE, type='load', target='content')
    sentences = corpus.article_to_sentences(target='segemented_participle_content')
    corpora = Corpora()
    corpora.word_to_vector(type='create', sentences=sentences, \
        path=PathManager.CORPORA_WORD2VEC)
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
    dictionary = corpora.word_dictionary(type='create', texts=texts, \
        path=PathManager.CORPORA_DICTIONARY)
    mmcorpus = corpora.article_texts_bow(type='create', texts=texts, dictionary=dictionary, \
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

def segement_content() :
    from basic.corpus import Corpus
    from file.path_manager import PathManager
    from simplifier.segementor import ContentSegementor
    corpus = Corpus()
    corpus.article_info(PathManager.CORPUS_ARTICLE)
    segementor = ContentSegementor(spst_path=PathManager.TOOLS_CONTENTSPST)
    corpus.segemented_list(PathManager.CORPUS_SENTENCE, type='create', target='content', \
        segementor=segementor)
    print 'finish'

def simplifying_content() :
    from basic.corpus import Corpus
    from file.path_manager import PathManager
    from simplifier.simplifier import ContentSimplifier
    corpus = Corpus()
    corpus.article_info(PathManager.CORPUS_SIMPLYARTICLE)
    corpus.segemented_list(PathManager.CORPUS_SENTENCE, type='load', target='content')
    simplifier = ContentSimplifier(redundance_path=PathManager.TOOLS_REDUNDANCE)
    corpus.simplify_content(simplifier=simplifier)
    corpus.article_info(PathManager.CORPUS_SIMPLYARTICLE)
    print 'finish'

def simplifying_title() :
    from file.path_manager import PathManager
    from basic.corpus import Corpus
    from basic.corpora import Corpora
    from simplifier.simplifier import TitleSimplifier
    corpus = Corpus()
    corpus.article_info(PathManager.CORPUS_SIMPLYARTICLE, type='load')
    corpus.segemented_participle_list(PathManager.CORPUS_SENTENCE, type='load', target='title')
    corpora = Corpora()
    dictionary = corpora.word_dictionary(type='load', path=PathManager.CORPORA_DICTIONARY)
    texts = corpora.article_texts_bow(type='load', path=PathManager.CORPORA_CONTENTTEXTS)
    tfidf = corpora.textsbow_to_tfidf(type='load', path=PathManager.CORPORA_TFIDF)
    simplifier = TitleSimplifier(word2vec_path=PathManager.CORPORA_WORD2VEC)
    corpus.simplify_title(dictionary, texts, tfidf, simplifier=simplifier)
    print 'finish'

def unique_article() :
    from file.path_manager import PathManager
    from basic.corpus import Corpus
    corpus = Corpus()
    corpus.article_info(PathManager.CORPUS_SIMPLYARTICLE, type='load')
    corpus.simplify_article()
    print 'finish'
 
def word_cluster() :
    from file.path_manager import PathManager
    from basic.corpus import Corpus
    from cluster.word_cluster import WordCluster
    from cluster.lda_cluster import LdaCluster
    corpus = Corpus()
    corpus.article_info(PathManager.CORPUS_SIMPLYARTICLE, type='load')
    cluster = WordCluster(corpus_path=PathManager.CORPORA_CONTENTTEXTS,  \
        tfidf_path=PathManager.CORPORA_TFIDF, \
        dict_path=PathManager.CORPORA_DICTIONARY, \
        w2v_path=PathManager.CORPORA_WORD2VEC, \
        lda_path=PathManager.CORPORA_LDA)
    cluster.read_test_label(data_path=PathManager.CLUSTER_TESTDATA)
    doc_topic_, topic_word_ = cluster.process(corpus.article_list)
    cluster.write_article_topic(doc_topic_, label_path=PathManager.CLUSTER_DOCTOPIC)
    cluster.write_article_topic(topic_word_, label_path=PathManager.CLUSTER_TOPICWORD)
    print 'finish'

def parsing() :
    from basic.corpora import Corpora
    from file.path_manager import PathManager
    from ltpparser.parsing import SentenceParsing
    from qa.article_tag import ArticleCluster
    corpus = SentenceParsing()
    # sentences = corpus.read_parsed(PathManager.CORPUS_SENTENCE)
    word_set = corpus.read_word(PathManager.CORPUS_SENTENCE)
    corpora = Corpora()
    word2vec = corpora.word_to_vector(type='load', path=PathManager.CORPORA_WORD2VEC)
    cluster = ArticleCluster()
    corpus.word_clustering(word2vec, word_set, cluster)
    print 'finish'

def unique() :
    from myunique.run import Corpus
    from file.path_manager import PathManager
    source_path = PathManager.CORPUS_ARTICLE
    title_path = PathManager.CORPUS_SPLIT
    unique_path = PathManager.CORPUS_SIMPLYARTICLE
    corpus = Corpus()
    corpus.run(source_path, title_path, \
        unique_path)

def segment() :
    from segment.run import Corpus
    from file.path_manager import PathManager
    source_path = PathManager.CORPUS_ARTICLE
    title_spst_path = PathManager.TOOLS_TITLESPST
    content_spst_path = PathManager.TOOLS_CONTENTSPST
    sentence_path = PathManager.CORPUS_SENTENCE
    seg_title_path = PathManager.CORPUS_SEGTITLE
    seg_content_path = PathManager.CORPUS_SEGCONTENT
    corpus = Corpus()
    corpus.run(source_path, title_spst_path, content_spst_path, \
        sentence_path, seg_title_path, seg_content_path)

def word_embedding() :
    from embedding.run import Corpus
    from file.path_manager import PathManager
    sentences_path = PathManager.CORPORA_MMCORPUS
    wordembed_path = PathManager.CORPORA_WORD2VEC
    word_cluster_path = PathManager.CLUSTER_WORDCLUSTER
    corpus = Corpus()
    corpus.run_create_word2vec(sentences_path, wordembed_path)

def word_bag() :
    from word.run import Corpus
    from file.path_manager import PathManager
    sentences_path = PathManager.CORPUS_SUBTITLE
    dictionary_path = PathManager.CORPORA_DICTIONARY
    corpus = Corpus()
    corpus.run_create_dictionary(sentences_path, \
        dictionary_path)
    
def pre_load() :
    from preload.run import Corpus
    from file.path_manager import PathManager
    sentences_path = PathManager.CORPUS_SUBTITLE
    json_path = PathManager.CORPORA_MMCORPUS
    corpus = Corpus()
    corpus.run_load_json(json_path)



if __name__ == '__main__' :
    # 5classifying()
    # simplifying_article()
    # tagging_article()
    # qa_system()
    # create_texts()
    # create_tfidf()
    # create_word2vec()
    # create_lda()
    # create_article_info()
    # find_synonymy()
    # filter_word()
    # feature_select()
    # create_classifier()
    # content_split_sentence()
    # simplifying_content()
    # simplifying_title()
    # word_cluster()
    # unique_article()
    # parsing()
    # unique()
    # segment()
    word_embedding()
    # word_bag()
    # pre_load()