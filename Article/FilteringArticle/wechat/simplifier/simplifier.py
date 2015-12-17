# -*- encoding = gb18030 -*-

# package importing start
import codecs
import numpy as np

from basic.article import Article
from basic.corpus import Corpus
from file.file_operator import TextFileOperator
# package importing end



class ContentSimplifier :

    def __init__(self, redundance_path='') :
        self.redundance_dict = self._read_dictionary(redundance_path)
        
    def _read_dictionary(self, split_path) :
        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(split_path)
        split_dict = dict()
        for data in data_list :
            if len(data) >= 1 :
                if data[0] not in split_dict :
                    split_dict[data[0]] = None
        return split_dict

    def tag_sentence(self, sentence) :
        """ Tag sentence as 0 or 1.
            if tag is 0 :
                sentence is redundance
            else :
                sentence is useful
        """
        redundance = False
        for word in self.redundance_dict :
            if word in sentence :
                redundance = True
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

    def __init__(self) :
        pass
                    
    def filter_sentence(self, sentences, words) :
        """ Filter sentence in sentences. """
        scores = [0]*len(sentences)
        for word in words :
            for idx, sentence in enumerate(sentences) :
                scores[idx] = [1 for latter in word if latter in sentence]
        if max(scores) != 0 :
            sentence = sentences[max(enumerate(scores), key=lambda x: x[1])[0]]
        else :
            sentence = ''
        return sentence
