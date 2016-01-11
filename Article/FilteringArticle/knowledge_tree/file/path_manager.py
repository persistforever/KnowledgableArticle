# -*- encoding = gb18030 -*-
""" Manager of project's global path """

# package importing start
import os
import ConfigParser
# package importing end


class PathManager :

    # a list of path
    TOOLS_TITLESPST = 'title splist in the tools'
    TOOLS_CONTENTSPST = 'sentence split in the tools'
    TOOLS_PUNCTUATION = 'punctuation in the tools'
    TOOLS_FIRSTPRO = 'first pronoun in the tools'
    TOOLS_SECONDPRO = 'second pronoun in the tools'
    TOOLS_THIRDPRO = 'third pronoun in the tools'
    TOOLS_KNOWLEDGEABLEWORD = 'knowledgeable word in the tools'
    TOOLS_POS = 'part of speech in the tools'
    TOOLS_REDUNDANCE = 'content redundance in the tools'
    
    SYNONYMYS_QUERY = 'query in the synonymys'
    SYNONYMYS_SYNONYMY = 'synonymy in the synonymys'
    
    BOWS_BOW = 'bag of word in bows'
    BOWS_WORD = 'word set in bows'
    BOWS_IDF = 'word idf in bows'

    CORPUS_ARTICLE = 'article list in corpus'
    CORPUS_SPLIT = 'split list in corpus'
    CORPUS_FEATURE = 'feature list in corpus'
    CORPUS_SENTENCE = 'sentence list in corpus'
    CORPUS_SUBTITLE = 'subtitle list in corpus'
    CORPUS_KEYWORD = 'keyword list in corpus'
    CORPUS_SIMPLYARTICLE = 'simply article list in corpus'
    CORPUS_UNIQUEARTICLE = 'unique article list in corpus'
    CORPUS_LUCENE = 'lucene result article list in corpus'
    CORPUS_KNOWLEDGE = 'knowledgeable article list in corpus'
    CORPUS_TRAINDATA = 'train data in corpus'
    CORPUS_SEGTITLE = 'segmented title in corpus'
    CORPUS_SEGCONTENT = 'segmented content in corpus'

    CORPORA_INFO = 'article info in corpora'
    CORPORA_DICTIONARY = 'dictionary in corpora accorrding to gensim'
    CORPORA_MMCORPUS = 'corpus in corpora stored as mmcorpus'
    CORPORA_TFIDF = 'tfidf model in corpora'
    CORPORA_WORD2TFIDF = 'word2sim by tfidf model initial file in the corpora'
    CORPORA_WORD2VEC = 'word2sim by word2vec model initial file in the corpora'
    CORPORA_WORDVECTOR = 'word vector in the corpora'
    CORPORA_LDA = 'lda model initial file in the corpora'
    CORPORA_TITLETEXTS = 'participle title texts in the corpora'
    CORPORA_CONTENTTEXTS = 'participle content texts in the corpora'

    CLASSIFIER_CLASSIFIER = 'classifier in the classifier'
    CLASSIFIER_TRAINDATA = 'training data in the classifier'
    CLASSIFIER_TESTDATA = 'testing data in the classifier'

    CLUSTER_TESTDATA = 'test data in the cluster'
    CLUSTER_DOCTOPIC = 'doc_topic in the cluster'
    CLUSTER_TOPICWORD = 'topic_word in the cluster'
    CLUSTER_WORDCLUSTER = 'word embedding test in the cluster'

    TAG_TAGTREE = 'tag tree in the tag'
    TAG_ARTICLETAG = 'article tag in the tag'
    TAG_SENTENCES = 'article sentences market in the tag'
    TAG_UNTAGSENTENCE = 'untag sentences market in the tag'
        
    @staticmethod
    def _get_configuration() :
        """ Get FILE_PATH of path manager. """
        cfg = ConfigParser.ConfigParser()
        cfg.read('knowledge_tree/file/configuration.ini')
        PathManager.TOOLS_TITLESPST = cfg.get('tools', 'TITLESPST')
        PathManager.TOOLS_CONTENTSPST = cfg.get('tools', 'CONTENTSPST')
        PathManager.TOOLS_PUNCTUATION = cfg.get('tools', 'PUNCTUATION')
        PathManager.TOOLS_FIRSTPRO = cfg.get('tools', 'FIRSTPRO')
        PathManager.TOOLS_SECONDPRO = cfg.get('tools', 'SECONDPRO')
        PathManager.TOOLS_THIRDPRO = cfg.get('tools', 'THIRDPRO')
        PathManager.TOOLS_KNOWLEDGEABLEWORD = cfg.get('tools', 'KNOWLEDGEABLEWORD')
        PathManager.TOOLS_POS = cfg.get('tools', 'POS')
        PathManager.TOOLS_REDUNDANCE = cfg.get('tools', 'REDUNDANCE')

        PathManager.SYNONYMYS_QUERY = cfg.get('synonymys', 'QUERY')
        PathManager.SYNONYMYS_SYNONYMY = cfg.get('synonymys', 'SYNONYMY')

        PathManager.BOWS_BOW = cfg.get('bows', 'BOW')
        PathManager.BOWS_WORD = cfg.get('bows', 'WORD')
        PathManager.BOWS_IDF= cfg.get('bows', 'IDF')

        PathManager.CORPUS_ARTICLE = cfg.get('corpus', 'ARTICLE')
        PathManager.CORPUS_SPLIT = cfg.get('corpus', 'SPLIT')
        PathManager.CORPUS_FEATURE = cfg.get('corpus', 'FEATURE')
        PathManager.CORPUS_SENTENCE = cfg.get('corpus', 'SENTENCE')
        PathManager.CORPUS_SUBTITLE = cfg.get('corpus', 'SUBTITLE')
        PathManager.CORPUS_KEYWORD = cfg.get('corpus', 'KEYWORD')
        PathManager.CORPUS_SIMPLYARTICLE = cfg.get('corpus', 'SIMPLYARTICLE')
        PathManager.CORPUS_UNIQUEARTICLE = cfg.get('corpus', 'UNIQUEARTICLE')
        PathManager.CORPUS_LUCENE = cfg.get('corpus', 'LUCENE')
        PathManager.CORPUS_KNOWLEDGE = cfg.get('corpus', 'KNOWLEDGE')
        PathManager.CORPUS_TRAINDATA = cfg.get('corpus', 'TRAINDATA')
        PathManager.CORPUS_SEGTITLE = cfg.get('corpus', 'SEGTITLE')
        PathManager.CORPUS_SEGCONTENT = cfg.get('corpus', 'SEGCONTENT')

        PathManager.CORPORA_INFO = cfg.get('corpora', 'INFO')
        PathManager.CORPORA_DICTIONARY = cfg.get('corpora', 'DICTIONARY')
        PathManager.CORPORA_MMCORPUS = cfg.get('corpora', 'MMCORPUS')
        PathManager.CORPORA_TFIDF = cfg.get('corpora', 'TFIDF')
        PathManager.CORPORA_WORD2TFIDF = cfg.get('corpora', 'WORD2TFIDF')
        PathManager.CORPORA_WORD2VEC = cfg.get('corpora', 'WORD2VEC')
        PathManager.CORPORA_WORDVECTOR = cfg.get('corpora', 'WORDVECTOR')
        PathManager.CORPORA_LDA = cfg.get('corpora', 'LDA')
        PathManager.CORPORA_TITLETEXTS = cfg.get('corpora', 'TITLETEXTS')
        PathManager.CORPORA_CONTENTTEXTS = cfg.get('corpora', 'CONTENTTEXTS')

        PathManager.CLASSIFIER_CLASSIFIER = cfg.get('classifier', 'CLASSIFIER')
        PathManager.CLASSIFIER_TRAINDATA = cfg.get('classifier', 'TRAINDATA')
        PathManager.CLASSIFIER_TESTDATA = cfg.get('classifier', 'TESTDATA')

        PathManager.CLUSTER_TESTDATA = cfg.get('cluster', 'TESTDATA')
        PathManager.CLUSTER_DOCTOPIC = cfg.get('cluster', 'DOCTOPIC')
        PathManager.CLUSTER_TOPICWORD = cfg.get('cluster', 'TOPICWORD')
        PathManager.CLUSTER_WORDCLUSTER = cfg.get('cluster', 'WORDCLUSTER')

        PathManager.TAG_TAGTREE = cfg.get('tag', 'TAGTREE')
        PathManager.TAG_ARTICLETAG = cfg.get('tag', 'ARTICLETAG')
        PathManager.TAG_SENTENCES = cfg.get('tag', 'SENTENCES')
        PathManager.TAG_UNTAGSENTENCE = cfg.get('tag', 'UNTAGSENTENCE')


PathManager._get_configuration()