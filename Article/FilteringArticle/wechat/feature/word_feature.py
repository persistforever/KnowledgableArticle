# -*- encoding = gb18030 -*-

# package importing start
from file.file_operator import TextFileOperator
from feature.base import BaseExtractor
# package importing end


class WordExtractor(BaseExtractor) :

    def __init__(self, firpro_path='', secpro_path='', thrpro_path='', word_path='') :
        BaseExtractor.__init__(self)

        self.firpro_dict = self._read_dictionary(firpro_path)
        self.secpro_dict = self._read_dictionary(secpro_path)
        self.thrpro_dict = self._read_dictionary(thrpro_path)
        self.word_dict = self._read_dictionary(word_path)
        
    def _read_dictionary(self, pro_path) :
        file_operator = TextFileOperator()
        data_list = file_operator.reading(pro_path)
        dictionary = dict()
        for data in data_list :
            if len(data) >= 1 :
                if data[0] not in dictionary :
                    dictionary[data[0]] = 0
        return dictionary
    
    def extractFeature(self, article_list) :
        for article in article_list :
            n_firpro, n_secpro, n_thrpro = 0, 0, 0
            n_title_name, n_title_time, n_title_place = 0, 0, 0
            n_content_name, n_content_time, n_content_place = 0, 0, 0
            n_knowldegeable_word = 0
            for word in article.split_title :
                if word.name in self.firpro_dict :
                    n_firpro += 1
                elif word.name in self.secpro_dict :
                    n_secpro += 1
                elif word.name in self.thrpro_dict :
                    n_thrpro += 1
                elif word.name in self.word_dict :
                    n_knowldegeable_word += 1
                if word.feature in [u'nrg', u'nrf'] :
                    n_title_name += 1
                if word.feature in [u't'] :
                    n_title_time += 1
                if word.feature in [u'ns'] :
                    n_title_place += 1
            for word in article.split_content :
                if word.name in self.firpro_dict :
                    n_firpro += 1
                elif word.name in self.secpro_dict :
                    n_secpro += 1
                elif word.name in self.thrpro_dict :
                    n_thrpro += 1
                if word.feature in [u'nrg', u'nrf'] :
                    n_content_name += 1
                if word.feature in [u't'] :
                    n_content_time += 1
                if word.feature in [u'ns'] :
                    n_content_place += 1
            article.set_features(n_firpro=n_firpro, n_secpro=n_secpro, n_thrpro=n_thrpro, \
                n_title_name=n_title_name, n_title_time=n_title_time, n_title_place=n_title_place, \
                n_content_name=n_content_name, n_content_time=n_content_time, \
                n_content_place=n_content_place, n_knowldegeable_word=n_knowldegeable_word)