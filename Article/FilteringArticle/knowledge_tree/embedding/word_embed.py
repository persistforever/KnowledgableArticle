# -*- encoding = gb18030 -*-

# package importing start
import re

import gensim

from file.file_operator import TextFileOperator
# package importing end


class WordEmbed :

    def __init__(self) :
        pass

    def word_to_vector(self,  type='create', sentences=[], path='') :
        """ If type is 'create' :
                Initialize the word2vec wordsim using sentences.
            If type is 'load' :
                Initialize the word2vec wordsim from the file.
        """
        if type is 'create' :
            word2vec_model = gensim.models.Word2Vec(sentences, size=100, window=5, min_count=1)
            word2vec_model.save(path)
        elif type is 'load' :
            word2vec_model = gensim.models.Word2Vec.load(path)
        print word2vec_model
        return word2vec_model

    def evaluate_word2vec_model(self, word2vec_model, word_dict) :
        """ Evaluate word2vec model accordding to word_dict.
            Score is sum distance outside cluster / sum distance among inside cluster.
        """
        score_fenzi = 0.0
        num_fenzi = 0.0
        score_fenmu = 0.0
        num_fenmu = 0.0
        similarity_list = []
        for worda in word_dict.keys() :
            for wordb in word_dict.keys() :
                if worda == wordb :
                    continue
                if worda in word2vec_model.index2word and \
                    wordb in word2vec_model.index2word :
                    distance = word2vec_model.similarity(worda, wordb)
                    similarity_list.append((worda + '&' + wordb, distance))
                    if word_dict[worda] == word_dict[wordb] :
                        score_fenzi += distance
                        num_fenzi += 1
                    else :
                        score_fenmu += distance
                        num_fenmu += 1
        if score_fenmu == 0.0 :
            return 0.0
        else :
            return score_fenzi / num_fenzi