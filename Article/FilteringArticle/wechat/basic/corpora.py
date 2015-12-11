# -*- encoding = gb18030 -*-

# package importing start
import math
import numpy as np

import gensim

from article import Article
from article import Word
from file.file_operator import BaseFileOperator, CSVFileOperator, TextFileOperator
# package importing end



class Corpora(object) :

    def __init__(self) :
        pass

    def create_gensim_dictionary(self, type='create', texts=[], path='') :
        """ If type is 'create' :
                Initialize the dictionary using texts and tokens.
                Texts is to initialize and Tokens is to filter.
            If type is 'load' :
                Initialize the dictionary from the file.
        """
        if type is 'create' :
            dictionary = gensim.corpora.Dictionary(texts)
            bad_ids, good_ids = [], []
            for word in dictionary.token2id.keys() :
                word_object = Word(word, sp_char='<:>')
                if self.word_remained(word_object) :
                    good_ids.append(dictionary.token2id[word_object.to_string()])
                else :
                    bad_ids.append(dictionary.token2id[word_object.to_string()])
            dictionary.filter_tokens(bad_ids, good_ids)
            dictionary.save(path)
        elif type is 'load' :
            dictionary = gensim.corpora.Dictionary.load(path)
        print dictionary
        return dictionary

    def create_gensim_corpus(self, type='create', texts=[], dictionary=None, path='') :
        """ If type is 'create' :
                Initialize the doc2bow using texts and dictionary
            If type is 'load' :
                Initialize the doc2bow from the file.
        """
        if type is 'create' :
            corpus = [dictionary.doc2bow(text) for text in texts]
            gensim.corpora.MmCorpus.serialize(path, corpus)
        elif type is 'load' :
            corpus = gensim.corpora.MmCorpus(path)
        print len(corpus)
        return corpus

    def create_gensim_tfidf(self,  type='create', mmcorpus=None, path='') :
        """ If type is 'create' :
                Initialize the tfidf model using mmcorpus
            If type is 'load' :
                Initialize the tfidf model from the file.
        """
        if type is 'create' :
            tfidf_model = gensim.models.TfidfModel(mmcorpus)
            tfidf_model.save(path)
        elif type is 'load' :
            tfidf_model = gensim.models.TfidfModel.load(path)
        print tfidf_model
        return tfidf_model

    def create_wordsim_tfidf(self,  type='create', mmcorpus=None, dictionary=None, \
        tfidf_model=None, path='') :
        """ If type is 'create' :
                Initialize the tfidf wordsim using mmcorpus
            If type is 'load' :
                Initialize the tfidf wordsim from the file.
        """
        if type is 'create' :
            tfidf_model = gensim.models.TfidfModel(mmcorpus)
            similarities = self._create_word_similarity(mmcorpus, dictionary, tfidf_model)
            gensim.corpora.SvmLightCorpus.serialize(path, similarities)
        elif type is 'load' :
            similarities = gensim.corpora.SvmLightCorpus(path)
        print len(similarities)
        return similarities

    def _create_word_similarity(self, mmcorpus, dictionary, tfidf_model) :
        """ create word similarities list. 
            Similarities is a [list] and each element is a [list].
            Each row in similarities is a word.
            Each column in word is the list of (word, similarity).
            Like this [ [(word_id, similarity), ...]
                        ...
                      ]
        """
        word_similarity = np.zeros([len(dictionary), len(dictionary)], dtype=float)
        word_mod = np.array([0] * len(dictionary))
        texts = [tfidf_model[text] for text in mmcorpus]
        for doc_id, text in enumerate(texts) :
            for idx_a in range(0, len(text)) :
                id_a = text[idx_a][0]
                for idx_b in range(idx_a+1, len(text)) :
                    id_b = text[idx_b][0]
                    word_similarity[id_a, id_b] += text[idx_a][1] * text[idx_b][1]
                word_mod[id_a] += text[idx_a][1] * text[idx_a][1]
        similarities = []
        for row in range(word_similarity.shape[0]) :
            for col in range(word_similarity.shape[1]) :
                if math.sqrt(word_mod[row]) != 0 and math.sqrt(word_mod[col]) != 0 :
                    word_similarity[row, col] = \
                        word_similarity[row, col] / (math.sqrt(word_mod[row]) * math.sqrt(word_mod[col]))
        for row in range(word_similarity.shape[0]) :
            similarity = []
            for col in range(row+1, word_similarity.shape[1]) :
                word_similarity[col, row] = word_similarity[row, col]
            for word_id, sim in enumerate(word_similarity[row, :].tolist()) :
                similarity.append((word_id, sim))
            similarities.append(similarity)
        return similarities

    def create_wordsim_word2vec(self,  type='create', sentences=[], path='') :
        """ If type is 'create' :
                Initialize the word2vec wordsim using sentences
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

    def word_remained(self, word) :
        # remain_pos = [u'z', u'vn', u'v', u's', u'nz', u'nt', u'ns', \
        #    u'n', u'j', u'd', u'b', u'an', u'ad', u'a']
        remain_pos = [u'vn', u'nz', u'nt', u'ns', u'n', u'an']
        if word.feature in remain_pos :
            return True
        else :
            return False

    def create_lda_model(self,  type='create', mmcorpus=None, dictionary=None, path='') :
        """ If type is 'create' :
                Initialize the lda model using mmcorpus and dictionary.
            If type is 'load' :
                Initialize the lda model from the file.
        """
        if type is 'create' :
            lda_model = gensim.models.ldamodel.LdaModel(corpus=mmcorpus, id2word=dictionary, \
                num_topics=3, iterations=1000)
            lda_model.save(path)
        elif type is 'load' :
            lda_model = gensim.models.ldamodel.LdaModel.load(path)
        print lda_model
        return lda_model