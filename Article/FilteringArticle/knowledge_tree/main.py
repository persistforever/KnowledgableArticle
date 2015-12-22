# -*- encoding = gb18030 -*-
"""
This python file is noly used to Debug.
Can call different function to do different tasks.
If function func_name debug finished, please complete the wechat/main/func_name.py.
"""

# package importing start
# package importing end


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
    dictionary_path = PathManager.CORPORA_DICTIONARY
    word_cluster_path = PathManager.CLUSTER_WORDCLUSTER
    similarity_path = PathManager.CLUSTER_TOPICWORD
    corpus = Corpus()
    corpus.run(sentences_path, dictionary_path, wordembed_path, word_cluster_path, \
        similarity_path)

def word_bag() :
    from word.run import Corpus
    from file.path_manager import PathManager
    sentences_path = PathManager.CORPUS_SUBTITLE
    dictionary_path = PathManager.CORPORA_DICTIONARY
    converted_sentences_path = PathManager.CORPORA_CONTENTTEXTS
    corpus = Corpus()
    corpus.run(sentences_path, dictionary_path, converted_sentences_path)
    
def pre_load() :
    from preload.run import Corpus
    from file.path_manager import PathManager
    sentences_path = PathManager.CORPUS_SUBTITLE
    dictionary_path = PathManager.CORPORA_DICTIONARY
    json_path = PathManager.CORPORA_MMCORPUS
    corpus = Corpus()
    corpus.run(sentences_path, dictionary_path, json_path)



if __name__ == '__main__' :
    # parsing()
    # unique()
    # segment()
    word_embedding()
    # word_bag()
    # pre_load()