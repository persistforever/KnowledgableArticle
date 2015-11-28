# -*- encoding = gb18030 -*-
""" Manager of project's global path """

# package importing start
import os
import ConfigParser
# package importing end


class PathManager :

    # a list of path
    TOOLS_WORD2VECTOR = 'word2vector initial file in the tools'
    SYNONYMYS_QUERY = 'query in the synonymys'
    SYNONYMYS_SYNONYMY = 'synonymy in the synonymys'
    BOWS_BOW = 'bag of word in bows'
    BOWS_WORD = 'word set in bows'
    CORPUS_ARTICLE = 'article list in corpus'
    CORPUS_SPLIT = 'split list in corpus'
    CORPORA_DICTIONARY = 'dictionary in copora accorrding to gensim'
        
    @staticmethod
    def _get_configuration() :
        """ Get FILE_PATH of path manager. """
        cfg = ConfigParser.ConfigParser()
        cfg.read('wechat/file/configuration.ini')
        PathManager.TOOLS_WORD2VEC = cfg.get('tools', 'WORD2VEC')
        PathManager.SYNONYMYS_QUERY = cfg.get('synonymys', 'QUERY')
        PathManager.SYNONYMYS_SYNONYMY = cfg.get('synonymys', 'SYNONYMY')
        PathManager.BOWS_BOW = cfg.get('bows', 'BOW')
        PathManager.BOWS_WORD = cfg.get('bows', 'WORD')
        PathManager.CORPUS_ARTICLE = cfg.get('corpus', 'ARTICLE')
        PathManager.CORPUS_SPLIT = cfg.get('corpus', 'SPLIT')
        PathManager.CORPORA_DICTIONARY = cfg.get('corpora', 'DICTIONARY')


PathManager._get_configuration()