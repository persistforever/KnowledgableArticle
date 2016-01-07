# -*- encoding = gb18030 -*-
"""
This python file is noly used to Debug.
Can call different function to do different tasks.
If function func_name debug finished, please complete the wechat/main/func_name.py.
"""

# package importing start
# package importing end


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
    wordvector_path = PathManager.CORPORA_WORDVECTOR
    corpus = Corpus()
    corpus.run(sentences_path, dictionary_path, wordembed_path, word_cluster_path, \
        similarity_path, wordvector_path)

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
    
def parsing() :
    from ltpparser.run import Corpus
    from file.path_manager import PathManager
    sentences_path = PathManager.CORPUS_SENTENCE
    dictionary_path = PathManager.CORPORA_DICTIONARY
    wordembed_path = PathManager.CORPORA_WORD2VEC
    word_cluster_path = PathManager.CLUSTER_WORDCLUSTER
    corpus = Corpus()
    corpus.run(sentences_path, dictionary_path, wordembed_path, word_cluster_path)
    print 'finish'
    
def appositive() :
    from appositive.run import Corpus
    from file.path_manager import PathManager
    sentences_path = PathManager.CORPUS_ARTICLE
    wordembed_path = PathManager.CORPORA_WORD2VEC
    appositive_path = PathManager.CORPUS_SPLIT
    corpus = Corpus()
    corpus.run(sentences_path, wordembed_path, appositive_path)
    print 'finish'
    
def tag() :
    from tag.run import Corpus
    from file.path_manager import PathManager
    sentences_path = PathManager.CORPUS_ARTICLE
    tag_tree_path = PathManager.TAG_TAGTREE
    tags_path = PathManager.TAG_ARTICLETAG
    tags_market_path = PathManager.TAG_ARTICLETAG
    sentences_market_path = PathManager.TAG_SENTENCES
    untag_sentence_path = PathManager.TAG_UNTAGSENTENCE
    corpus = Corpus()
    corpus.run(sentences_path, tag_tree_path, sentences_market_path, tags_path, \
        tags_market_path, untag_sentence_path)
    print 'finish'
    
def pre_treate() :
    from pretreate.run import Corpus
    from file.path_manager import PathManager
    articles_path = PathManager.CORPUS_ARTICLE
    participle_title_path = PathManager.CORPUS_SPLIT
    treated_article_path = PathManager.CORPUS_FEATURE
    corpus = Corpus()
    corpus.run(articles_path, participle_title_path, treated_article_path)


if __name__ == '__main__' :
    # unique()
    # segment()
    # word_embedding()
    # word_bag()
    # pre_load()
    # parsing()
    # appositive()
    # tag()
    pre_treate()