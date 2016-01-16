# -*- encoding = gb18030 -*-
"""
This python file is noly used to Debug.
Can call different function to do different tasks.
If function func_name debug finished, please complete the wechat/main/func_name.py.
"""

# package importing start
# package importing end


    
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
    
def pretreate() :
    from pretreate.run import Corpus
    from file.path_manager import PathManager
    articles_path = PathManager.CORPUS_ARTICLE
    participle_title_path = PathManager.CORPUS_SPLIT
    treated_article_path = PathManager.CORPUS_FEATURE
    corpus = Corpus()
    corpus.run(articles_path, participle_title_path, treated_article_path)
    
def classify() :
    from classify.run import Corpus
    from file.path_manager import PathManager
    articles_path = PathManager.CORPUS_ARTICLE
    # participles_path = PathManager.CORPUS_SPLIT
    article_market_path = PathManager.CORPUS_SUBTITLE
    feature_path = PathManager.CORPUS_FEATURE
    feature_market_path = PathManager.CORPUS_SENTENCE
    pos_path = PathManager.TOOLS_POS
    punc_path = PathManager.TOOLS_PUNCTUATION
    klword_path = PathManager.TOOLS_KNOWLEDGEABLEWORD
    train_path = PathManager.CLASSIFIER_TRAINDATA
    test_path = PathManager.CLASSIFIER_TESTDATA
    corpus = Corpus()
    corpus.run(articles_path, article_market_path, \
        pos_path, punc_path, klword_path, feature_path, feature_market_path, \
        train_path, test_path)
    
def embedding() :
    from embedding.run import Corpus
    from file.path_manager import PathManager
    articles_path = PathManager.CORPUS_ARTICLE
    participle_title_path = PathManager.CORPUS_SPLIT
    sentences_path = PathManager.CORPUS_KEYWORD
    word_embedding_path =PathManager.CORPUS_SIMPLYARTICLE
    corpus = Corpus()
    corpus.run(articles_path, participle_title_path, sentences_path, sentences_path, \
        word_embedding_path, word_embedding_path)


if __name__ == '__main__' :
    # tag()
    # pretreate()
    classify()
    # embedding()