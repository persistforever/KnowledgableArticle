# -*- encoding = gb18030 -*-
""" Manager of project's global path """

# package importing start
import os
import ConfigParser
# package importing end


class PathManager :

    # a list of path
    TOOLS_TITLESPST = 'title splist sentence in the synonymys'
    SYNONYMYS_QUERY = 'query in the synonymys'
    SYNONYMYS_SYNONYMY = 'synonymy in the synonymys'
    BOWS_BOW = 'bag of word in bows'
    BOWS_WORD = 'word set in bows'
    BOWS_IDF = 'word idf in bows'
    CORPUS_ARTICLE = 'article list in corpus'
    CORPUS_SPLIT = 'split list in corpus'
    CORPUS_SENTENCE = 'sentence list in corpus'
    CORPUS_SUBTITLE = 'subtitle list in corpus'
    CORPUS_KEYWORD = 'keyword list in corpus'
    CORPUS_SIMPLYARTICLE = 'simply article list in corpus'
    CORPUS_UNIQUEARTICLE = 'unique article list in corpus'
    CORPUS_LUCENE = 'lucene result article list in corpus'
    CORPORA_DICTIONARY = 'dictionary in corpora accorrding to gensim'
    CORPORA_MMCORPUS = 'corpus in corpora stored as mmcorpus'
    CORPORA_TFIDF = 'tfidf model in corpora'
    CORPORA_WORD2TFIDF = 'word2sim by tfidf model initial file in the corpora'
    CORPORA_WORD2VEC = 'word2sim by word2vec model initial file in the corpora'
        
    @staticmethod
    def _get_configuration() :
        """ Get FILE_PATH of path manager. """
        cfg = ConfigParser.ConfigParser()
        cfg.read('wechat/file/configuration.ini')
        PathManager.TOOLS_TITLESPST = cfg.get('tools', 'TITLESPST')
        PathManager.SYNONYMYS_QUERY = cfg.get('synonymys', 'QUERY')
        PathManager.SYNONYMYS_SYNONYMY = cfg.get('synonymys', 'SYNONYMY')
        PathManager.BOWS_BOW = cfg.get('bows', 'BOW')
        PathManager.BOWS_WORD = cfg.get('bows', 'WORD')
        PathManager.BOWS_IDF= cfg.get('bows', 'IDF')
        PathManager.CORPUS_ARTICLE = cfg.get('corpus', 'ARTICLE')
        PathManager.CORPUS_SPLIT = cfg.get('corpus', 'SPLIT')
        PathManager.CORPUS_SENTENCE = cfg.get('corpus', 'SENTENCE')
        PathManager.CORPUS_SUBTITLE = cfg.get('corpus', 'SUBTITLE')
        PathManager.CORPUS_KEYWORD = cfg.get('corpus', 'KEYWORD')
        PathManager.CORPUS_SIMPLYARTICLE = cfg.get('corpus', 'SIMPLYARTICLE')
        PathManager.CORPUS_UNIQUEARTICLE = cfg.get('corpus', 'UNIQUEARTICLE')
        PathManager.CORPUS_LUCENE = cfg.get('corpus', 'LUCENE')
        PathManager.CORPORA_DICTIONARY = cfg.get('corpora', 'DICTIONARY')
        PathManager.CORPORA_MMCORPUS = cfg.get('corpora', 'MMCORPUS')
        PathManager.CORPORA_TFIDF = cfg.get('corpora', 'TFIDF')
        PathManager.CORPORA_WORD2TFIDF = cfg.get('corpora', 'WORD2TFIDF')
        PathManager.CORPORA_WORD2VEC = cfg.get('corpora', 'WORD2VEC')


PathManager._get_configuration()