# -*- encoding = gb18030 -*-

# package importing start
import gensim

from synonymy.base import SynonymySearcherBase
from file.path_manager import PathManager
from basic.word import Word
# package importing end


class Word2Vector(SynonymySearcherBase) :

    def __init__(self, n_most=10, w2v_path='') :
        SynonymySearcherBase.__init__(self)

        self.w2v_path = w2v_path
        self.vector_model = self._read_model()
        self.n_most = n_most
        self.n_condidate = 5 * self.n_most

    def _read_model(self) :
        """ Read word2vector models. """
        vector_model = gensim.models.Word2Vec.load(self.w2v_path)
        return vector_model

    def find_synonymy_words(self) :
        """ find synonymy words of the query_list. 
            This is a abstract function and MUST override (now overriding).
            Return the synonymy word list. 
        """
        condidate_dict = dict()
        for query_word in self.query_list :
            synonymy_list = self.vector_model.most_similar( \
                query_word.to_string(), topn=self.n_condidate)
            for word_name, similarity in synonymy_list :
                word = Word(word_name, sp_char='<:>')
                if word.to_string() not in condidate_dict :
                    condidate_dict[word.to_string()] = []
                condidate_dict[word.to_string()].append(similarity)
        for condidate in condidate_dict.keys() :
            value_list = condidate_dict[condidate]
            condidate_dict[condidate] = 1.0 * sum(value_list) / len(value_list)
        condidate_list = sorted(condidate_dict.iteritems(), \
            key=lambda x: x[1], reverse=True)
        for condidate, sc in condidate_list[0:self.n_most] :
            word = Word(condidate, sp_char='<:>')
            word.set_params(score=sc)
            self.synonymy_list.append(word)