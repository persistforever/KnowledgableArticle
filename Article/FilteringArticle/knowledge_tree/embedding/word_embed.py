# -*- encoding = gb18030 -*-

# package importing start
import re
import numpy as np

import gensim

from file.file_operator import TextFileOperator
# package importing end


class WordEmbed :

    def __init__(self) :
        pass

    def word_to_vector(self,  type='create', sentences=list(), path='') :
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

    def evaluate_word2vec_model(self, dictionary, word2vec_model, word_dict, word_list) :
        """ Evaluate word2vec model accordding to word_dict.
            Score is sum distance outside cluster / sum distance among inside cluster.
        """
        score_fenzi = 0.0
        num_fenzi = 0.0
        score_fenmu = 0.0
        num_fenmu = 0.0
        similarity_list = []
        similarity_matrix = np.zeros([len(word_list), len(word_list)])
        index2word = dict((value, key) for key, value in dictionary.iteritems())
        for idxa, wa in enumerate(word_list) :
            for idxb, wb in enumerate(word_list) :
                if wa == wb :
                    continue
                if wa in dictionary and wb in dictionary :
                    worda = str(dictionary[wa])
                    wordb = str(dictionary[wb])
                    if worda in word2vec_model.index2word and \
                        wordb in word2vec_model.index2word :
                        similarity = word2vec_model.similarity(worda, wordb)
                        similarity_list.append((worda + '&' + wordb, similarity))
                        similarity_matrix[idxa, idxb] = similarity
                        if word_dict[wa] == word_dict[wb] :
                            score_fenzi += similarity
                            num_fenzi += 1
                        else :
                            score_fenmu += similarity
                            num_fenmu += 1
        score = 0.0
        if score_fenmu != 0.0 :
            score = (score_fenzi / num_fenzi) / (score_fenmu / num_fenmu)
        return score, similarity_matrix

    def remove_stop_words(self, type='create', dictionary=dict(), sentences=list()) :
        """ If type is 'create' :
                Convert to gensim dictionary and find stop words.
            If type is 'load' :
                Load stop words from file.
        """
        index2word = dict((value, key) for key, value in dictionary.iteritems())
        if type == 'load' :
            diction = gensim.corpora.Dictionary(sentences)
            word_dfs = sorted(diction.dfs.iteritems(), key=lambda x: x[1], reverse=True)
            print diction
            return diction
        elif type == 'create' :
            removed_pos = [u'w', u'r', u'u', u'm', u'p', u'c', u'd', u'f']
            rmstop_sentences = []
            for sentence in sentences :
                rmstop_sentence = []
                for word in sentence :
                    if index2word[int(word)].split('<:>')[1] not in removed_pos :
                        rmstop_sentence.append(word)
                rmstop_sentences.append(rmstop_sentence)
            return rmstop_sentences

    def get_word2vec_model(self, word2vec_model) :
        """ Write word2vec model into file.
            Each row is a word.
            Each column is the entry of the embedding.
        """
        word_list = list()
        for word in word2vec_model.index2word :
            row = [word]
            row.extend(word2vec_model[word])
            word_list.append(row)
        return word_list