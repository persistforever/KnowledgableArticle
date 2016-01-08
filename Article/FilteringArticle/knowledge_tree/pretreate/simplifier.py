# -*- encoding = gb18030 -*-

# package importing start
import codecs
import numpy as np
import re

from file.file_operator import TextFileOperator
# package importing end



class ContentSimplifier :

    def __init__(self) :
        pass

    def tag_sentence(self, sentence) :
        """ Tag sentence as 0 or 1.
            if tag is 0 :
                sentence is redundance
            else :
                sentence is useful
        """
        patterns = [re.compile(p) for p in [u'(微信)', u'(点击).*(关注)', u'(长按复制)', u'(阅读原文)', \
                                            u'(订阅)', u'(分享)', u'(二维码)', u'(回复)', u'(QQ)']]
        redundance = False
        for pattern in patterns :
            if pattern.search(sentence) :
                redundance = True
                break
        return (sentence, redundance)

    def filter_tail(self, sentence_list) :
        """ Filter redundance in tail.
            redundance score of each sentence is bottom redundance rate.
        """
        n_redundance = 0
        n_sentence = 0
        sentence_score_list = []
        for idx in range(len(sentence_list)-1, -1, -1) :
            redundance_score = 0.0
            n_sentence += 1
            if sentence_list[idx][1] == True :
                n_redundance += 1
                redundance_score = 1.0*n_redundance/n_sentence
            sentence = (sentence_list[idx][0], redundance_score)
            sentence_score_list.append(sentence)
        sentence_score_list.reverse()
        needed = False
        for idx, sentence in enumerate(sentence_score_list) :
            if sentence[1] >= 0.5 :
                needed = True
                break
        if needed :
            return sentence_list[0:idx]
        else :
            return sentence_list

    def filter_head(self, sentence_list) :
        """ Filter redundance in head.
            redundance score of each sentence is above redundance rate.
        """
        n_redundance = 0
        n_sentence = 0
        sentence_score_list = []
        for idx in range(0, len(sentence_list)) :
            redundance_score = 0.0
            n_sentence += 1
            if sentence_list[idx][1] == True :
                n_redundance += 1
                redundance_score = 1.0*n_redundance/n_sentence
            sentence = (sentence_list[idx][0], redundance_score)
            sentence_score_list.append(sentence)
        needed = False
        for idx in range(len(sentence_score_list)-1, -1, -1) :
            if sentence_score_list[idx][1] >= 0.5 :
                needed = True
                break
        if needed :
            return sentence_list[idx+1:]
        else :
            return sentence_list

        
class TitleSimplifier :

    def __init__(self, word2vec_path='') :
        self.word2vec = gensim.models.Word2Vec.load(word2vec_path)
                    
    def filter_sentence(self, sentences, words) :
        """ Filter sentence in sentences. """
        scores = [0]*len(sentences)
        for word in words :
            for idx, sentence in enumerate(sentences) :
                fenmu = 0
                for worda in sentence :
                    worda = worda.to_string()
                    if worda in self.word2vec :
                        fenmu += 1
                        for wordb in words :
                            if wordb in self.word2vec :
                                scores[idx] += self.word2vec.similarity(worda, wordb)
                if fenmu == 0 :
                    scores[idx] = 0
                else :
                    scores[idx] /= 1.0 * fenmu
        if max(scores) != 0 :
            sentence = sentences[max(enumerate(scores), key=lambda x: x[1])[0]]
        else :
            sentence = ''
        return sentence
