dictionary='E:/data/knowledge/corpora/run/fashion/dictionary.txt'
mmcorpus='E:/data/knowledge/corpora/run/fashion/mmcorpus.txt'
tfidf_model='E:/data/knowledge/corpora/run/fashion/tfidf.txt'
word_sim='E:/data/knowledge/corpora/run/fashion/wordsim_tfidf.txt'
python E://github/KnowledgableArticle/Article/FilteringArticle/wechat/main/corpora/create_wordsim.py $dictionary $mmcorpus $tfidf_model $word_sim