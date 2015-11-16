# -*- encoding = utf8 -*-
'''
topic model
'''

import codecs
import numpy as np
import lda
from BasicClass import Article


class LDA :

    def constrTree(self, artlist) :
        worddict = dict()
        for article in artlist :
            for word in article.keyword :
                worddict[word[0].name] = None
        idx = 0
        for word in worddict :
            worddict[word] = idx
            idx += 1
        vocab = [t[0] for t in sorted(worddict.iteritems(), key=lambda x: x[1], reverse=False)]
        X = []
        for article in artlist :
            article.artvector = [0]*idx
            for word in article.keyword :
                article.artvector[worddict[word[0].name]] += 1
            X.append(np.array(article.artvector))
        X = np.array(X)
        model = lda.LDA(n_topics=10, n_iter=1000, random_state=1).fit(X)
        topic_word = model.topic_word_
        for idx in range(len(model.doc_topic_)) :
            artlist[idx].topiclist = model.doc_topic_[idx, :].tolist()
        n_top_words = 20
        topiclist = []
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
            topiclist.append(topic_words)
        return topiclist