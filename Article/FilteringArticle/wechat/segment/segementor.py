# -*- encoding = gb18030 -*-

# package importing start
import re

from file.file_operator import TextFileOperator
# package importing end


class BaseSegementor :

    def __init__(self, spst_path='') :
        self.split_dict = self._read_dictionary(spst_path)
        
    def _read_dictionary(self, split_path) :
        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(split_path)
        split_dict = dict()
        for data in data_list :
            if len(data) >= 1 :
                if data[0] not in split_dict :
                    split_dict[data[0]] = None
        return split_dict


class ContentSegementor(BaseSegementor) :

    def __init__(self, spst_path='') :
        BaseSegementor.__init__(self, spst_path)

    def segement(self, sentence) :
        """ Split content into sentence. """
        self.split_char = '['
        for sp in self.split_dict :
            self.split_char += sp + '|'
        self.split_char += u'\u3000' + '|'
        self.split_char += ']'
        segemented_sentence = []
        for sent in re.split(self.split_char, sentence) :
            if sent.strip() != '' :
                segemented_sentence.append(sent)
        return segemented_sentence

    
class TitleSegementor(BaseSegementor) :

    def __init__(self, spst_path='') :
        BaseSegementor.__init__(self, spst_path)

    def segement(self, sentence) :
        """ Split content into sentence. """
        self.split_char = '['
        for sp in self.split_dict :
            self.split_char += sp + '|'
        self.split_char += ']'
        segemented_sentence = []
        for sent in re.split(self.split_char, sentence) :
            if sent.strip() != '' :
                segemented_sentence.append(sent)
        return segemented_sentence