dictionary='E:/data/knowledge/corpora/run/fashion/dictionary.txt'
mmcorpus='E:/data/knowledge/corpora/run/fashion/mmcorpus.txt'
tfidf_model='E:/data/knowledge/corpora/run/fashion/tfidf.txt'
lda_model='E:/data/knowledge/corpora/run/fashion/lda/lda_5topics.txt'
num='5'
python E://github/KnowledgableArticle/Article/FilteringArticle/wechat/main/corpora/create_lda.py $dictionary $mmcorpus $tfidf_model $lda_model $num