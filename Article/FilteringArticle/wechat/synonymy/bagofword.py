# -*- encoding = gb18030 -*-

# package importing start
import gensim

from synonymy.base import SynonymySearcherBase
from file.path_manager import PathManager
from file.file_operator import TextFileOperator
from basic.word import Word
# package importing end


class BagOfWord(SynonymySearcherBase) :

    def __init__(self, n_most=10, bow_path=PathManager.TOOLS_WORD2VEC, \
        word_path=PathManager.TOOLS_WORD2VEC) :
        SynonymySearcherBase.__init__(self)

        self.bow_path = bow_path
        self.n_most = n_most
        self.n_condidate = 5 * self.n_most

    def _read_model(self) :
        """ Read bagofword models. """
        vector_model = gensim.models.Word2Vec.load(self.w2v_path)
        return vector_model

    def read_word(self, word_path=PathManager.BOWS_WORD) :
        """ Read word bag. 
            Each row of the file is a word.
            column[0] of the file is the word and feature
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(word_path)
        for data in data_list :
            if len(data[0].split(':')) >= 2 :
                word = Word(data[0])
                data[0] = word.to_string()
            else :
                del data
        file_operator.writing(word_path)

    def find_synonymy_words(self) :
        """ find synonymy words of the query_list. 
            This is a abstract function and MUST override (now overriding).
            Return the synonymy word list. 
        """
        condidate_dict = dict()
        for query_word in self.query_list :
            synonymy_list = self.vector_model.most_similar( \
                query_word.name.encode('utf8'), topn=self.n_condidate)
            for word_name, similarity in synonymy_list :
                word = Word(word_name.decode('utf8'))
                if word.to_string() not in condidate_dict :
                    condidate_dict[word.to_string()] = []
                condidate_dict[word.to_string()].append(similarity)
        for condidate in condidate_dict.keys() :
            value_list = condidate_dict[condidate]
            condidate_dict[condidate] = 1.0 * sum(value_list) / len(value_list)
        condidate_list = sorted(condidate_dict.iteritems(), \
            key=lambda x: x[1], reverse=True)
        for condidate, sc in condidate_list[0:self.n_most] :
            word = Word(condidate)
            word.set_params(score=sc)
            self.synonymy_list.append(word)