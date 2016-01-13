# -*- encoding = gb18030 -*-

# package importing start
import numpy as np
import re

from file.file_operator import TextFileOperator
# package importing end


class BaseExtractor :
    
    def __init__(self) :
        pass
    
    def extract_feature(self, article) :
        """ Extract feature of the article. """
        pass


class PosExtractor(BaseExtractor) :

    def __init__(self, pos_path, w=20, combined=False) :
        BaseExtractor.__init__(self)
        
        self.pos_dict = self._read_dictionary(pos_path)
        self.w = w
        noun = [5, 11, 12, 14, 37]
        time = [16]
        place = [15]
        name = [19, 20]
        adjective = [3, 22, 23, 28]
        verb = [2, 4, 29, 45]
        adverb = [9, 27]
        conjunction = [24, 39]
        mood = [36, 46, 10]
        quantity = [34, 38, 27, 18]
        if combined :
            self.cluster = [noun, time, place, name, adjective, verb, adverb, conjunction, mood, quantity]
        else :
            self.cluster = [range(len(self.pos_dict))]
        
    def _read_dictionary(self, pos_path) :
        file_operator = TextFileOperator()
        data_list = file_operator.reading(pos_path)
        dictionary = dict()
        for data in data_list :
            if len(data) >= 1 :
                dictionary[data[0]] = 0
        return dictionary
    
    def extract_feature(self, participle_content) :
        num_list = list()
        for x in range(0, min(len(participle_content), 500) - self.w + 1) :
            pos_hist = dict()
            for key in self.pos_dict.keys() :
                pos_hist[key] = 0
            for i in range(x, x + self.w) :
                if participle_content[i].feature in pos_hist :
                    pos_hist[participle_content[i].feature] += 1
            num_list.append(pos_hist.values())
        mean_set, var_set = list(), list()
        for j in range(len(num_list[0])) :
            mean_set.append(np.mean([line[j] for line in num_list]))
            var_set.append(np.var([line[j] for line in num_list]))
        value_list = [0.0] * (2*len(self.cluster))
        for index, term in enumerate(self.cluster) :
            for idx in term :
                value_list[index] += mean_set[idx]
                value_list[index+len(self.cluster)] += var_set[idx]
        return value_list


class TokenExtractor(BaseExtractor) :
    
    def __init__(self, pc_path) :
        BaseExtractor.__init__(self)

        self.split_dict = dict().fromkeys([u'\u3002', u'\uff01', u'\uff1f'])
        self.punc_dict = self._read_dictionary(pc_path)
        
    def _read_dictionary(self, pro_path) :
        file_operator = TextFileOperator()
        data_list = file_operator.reading(pro_path)
        dictionary = dict()
        for data in data_list :
            if len(data) >= 1 :
                if data[0] not in dictionary :
                    dictionary[data[0]] = 0
        return dictionary
    
    def extract_feature(self, title, content, participle_title, participle_content) :
        title_length = len(title)
        content_length = len(content)
        n_title_word = len(participle_title) 
        n_content_word = len(participle_content)
        titleword_dict = dict()
        for word in participle_title :
            if word.name not in titleword_dict :
                titleword_dict[word.name] = None
        contentword_dict = dict()
        for word in participle_content :
            if word.name not in contentword_dict :
                contentword_dict[word.name] = None
        n_dist_title_word = len(titleword_dict)
        n_dist_content_word = len(contentword_dict)
        n_title_punc = len([char for char in title if char in self.punc_dict])
        n_content_punc = len([char for char in content if char in self.punc_dict])
        paragraph_split_char = u'[\u3000]'
        paragraph_list = re.split(paragraph_split_char, content)
        n_paragraph = len(paragraph_list)
        sentence_split_char = u'['
        for sp in self.split_dict :
            sentence_split_char += sp + u'|'
        sentence_split_char += u']'
        n_sentence = 0
        avg_sentence_lenght = 0.0
        avg_paragraph_lenght = 0.0
        for paragraph in paragraph_list :
            sentence_list = re.split(sentence_split_char, paragraph)
            n_sentence += len(sentence_list)
            avg_paragraph_lenght += len(sentence_list)
            for sentence in sentence_list :
                avg_sentence_lenght += len(sentence)
        avg_sentence_lenght /= 1.0 * n_sentence
        avg_paragraph_lenght /= 1.0 * n_paragraph
        return [title_length, content_length, n_title_word, \
            n_content_word, n_dist_title_word, n_dist_content_word, n_title_punc, \
            n_content_punc, n_paragraph, n_sentence, avg_sentence_lenght, avg_paragraph_lenght]
            

class UserExtractor(BaseExtractor) :

    def __init__(self) :
        BaseExtractor.__init__(self)
    
    def extract_feature(self, article) :
        n_zan = article['n_zan']
        n_forward = article['n_forward']
        n_click = article['n_click']
        n_collect = article['n_collect']
        read_time = article['read_time']
        finish_rate = article['finish_rate']
        return [n_zan, n_forward, n_click, n_collect, read_time, finish_rate]


class WordExtractor(BaseExtractor) :

    def __init__(self, word_path, weight=1) :
        BaseExtractor.__init__(self)

        self.weight = 1
        self.firpro_dict = dict().fromkeys([u'\u6211', u'\u54b1'])
        self.secpro_dict = dict().fromkeys([u'\u4f60', u'\u60a8'])
        self.thrpro_dict = dict().fromkeys([u'\u4ed6', u'\u5979', u'\u5b83'])
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
    
    def extract_feature(self, participle_title, participle_content) :
        n_firpro, n_secpro, n_thrpro = 0, 0, 0
        n_title_name, n_title_time, n_title_place = 0, 0, 0
        n_content_name, n_content_time, n_content_place = 0, 0, 0
        n_knowldegeable_word = 0
        for word in participle_title :
            if word.name in self.firpro_dict :
                n_firpro += self.weight
            elif word.name in self.secpro_dict :
                n_secpro += self.weight
            elif word.name in self.thrpro_dict :
                n_thrpro += self.weight
            elif word.name in self.word_dict :
                n_knowldegeable_word += self.weight
            if word.feature in [u'nrg', u'nrf'] :
                n_title_name += self.weight
            if word.feature in [u'nt'] :
                n_title_time += self.weight
            if word.feature in [u'ns'] :
                n_title_place += self.weight
        for word in participle_content :
            if word.name in self.firpro_dict :
                n_firpro += 1
            elif word.name in self.secpro_dict :
                n_secpro += 1
            elif word.name in self.thrpro_dict :
                n_thrpro += 1
            if word.feature in [u'nrg', u'nrf'] :
                n_content_name += 1
            if word.feature in [u'nt'] :
                n_content_time += 1
            if word.feature in [u'ns'] :
                n_content_place += 1
        return [n_firpro, n_secpro, n_thrpro, \
            n_title_name, n_title_time, n_title_place, n_content_name, \
            n_content_time, n_content_place, n_knowldegeable_word]