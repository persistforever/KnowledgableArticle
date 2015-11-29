# -*- encoding = gb18030 -*-

# package importing start
import gensim

from synonymy.base import SynonymySearcherBase
from file.path_manager import PathManager
from file.file_operator import TextFileOperator
from basic.word import Word
# package importing end


class BagOfWord(SynonymySearcherBase) :

    def __init__(self, mmcps_path='', dict_path='', n_most=10) :
        SynonymySearcherBase.__init__(self)

        self.mmcps_path = mmcps_path
        self.dict_path = dict_path
        self.n_most = n_most
        self.n_condidate = 5 * self.n_most
        self.mmcorpus, self.dictionary = self._read_model()

    def _read_model(self) :
        """ Read bagofword models. """
        mmcorpus = gensim.corpora.MmCorpus(self.mmcps_path)
        dictionary = gensim.corpora.Dictionary.load(self.dict_path)
        return mmcorpus, dictionary

    def find_synonymy_words(self) :
        """ find synonymy words of the query_list. 
            This is a abstract function and MUST override (now overriding).
            Return the synonymy word list. 
        """
        tfidf_model = gensim.models.TfidfModel(self.mmcorpus)
        '''
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
        '''

    def similarity(self, worda, wordb) :
        ida = self.dictionary.token2id[worda]
        idb = self.dictionary.token2id[wordb]
        