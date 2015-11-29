# -*- encoding = gb18030 -*-

# package importing start
import numpy as np
import math

import gensim

from synonymy.base import SynonymySearcherBase
from file.path_manager import PathManager
from file.file_operator import TextFileOperator
from basic.word import Word
# package importing end


class BagOfWord(SynonymySearcherBase) :

    def __init__(self, n_most=10, w2t_path='', dict_path = '') :
        SynonymySearcherBase.__init__(self)

        self.w2t_path = w2t_path
        self.dict_path = dict_path
        self.word_similarity, self.dictionary = self._read_model()
        self.n_most = n_most
        self.n_condidate = 5 * self.n_most

    def _read_model(self) :
        """ Read word2tfidf models. 
            Create word similarity matrix.
        """
        word2tfidf = gensim.corpora.SvmLightCorpus(self.w2t_path)
        word_similarity = np.zeros([len(word2tfidf), len(word2tfidf)], dtype=float)
        for idx_a, text in enumerate(word2tfidf) :
            for idx_b, similarity in text :
                word_similarity[idx_a, idx_b] = similarity
        dictionary = gensim.corpora.Dictionary.load(self.dict_path)
        return word_similarity, dictionary

    def most_similar(self, query_word, topn=10) :
        """ return query's most similar topn words. 
            This like gensim.word2vec.most_similar().
        """
        query_word_id = self.dictionary.token2id[query_word.decode('utf8')]
        sorted_similar_word = sorted(enumerate(self.word_similarity[query_word_id, :].tolist()), \
            key=lambda x:x[1], reverse=True)
        top_similar_word = []
        for word_id, similarity in sorted_similar_word[0:topn] :
            top_similar_word.append([self.dictionary[word_id].encode('utf8'), similarity])
        return top_similar_word

    def find_synonymy_words(self) :
        """ find synonymy words of the query_list. 
            This is a abstract function and MUST override (now overriding).
            Return the synonymy word list. 
        """
        condidate_dict = dict()
        for query_word in self.query_list :
            try :
                synonymy_list = self.most_similar( \
                    query_word.to_string().encode('utf8'), topn=self.n_condidate)
                for word_name, similarity in synonymy_list :
                    word = Word(word_name.decode('utf8'), sp_char='<:>')
                    if word.to_string() not in condidate_dict :
                        condidate_dict[word.to_string()] = []
                    condidate_dict[word.to_string()].append(similarity)
            except Exception, e :
                pass
        for condidate in condidate_dict.keys() :
            value_list = condidate_dict[condidate]
            condidate_dict[condidate] = 1.0 * sum(value_list) / len(value_list)
        condidate_list = sorted(condidate_dict.iteritems(), \
            key=lambda x: x[1], reverse=True)
        for condidate, sc in condidate_list[0:self.n_most] :
            word = Word(condidate, sp_char='<:>')
            word.set_params(score=sc)
            self.synonymy_list.append(word)