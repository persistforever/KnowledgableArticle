# -*- encoding = gb18030 -*-

# package importing start
import re

from file.file_operator import TextFileOperator
# package importing end


class SentenceSpliter :
    """ Split content into sub_sentence.
        Input :
            1. sentence split path : a file that each line is a split char.
            2. content : a string to split.
        Output :
            1. sub_sentence_list : a list that each element is a splited sentence.
    """

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

    def split_content(self, content) :
        """ Split content into sentence. """
        split_char = '['
        for sp in self.split_dict :
            split_char += sp + '|'
        split_char += u'\u3000' + '|'
        split_char += ']'
        sub_sentence_list = []
        for sentence in re.split(split_char, content) :
            if sentence.strip() != '' :
                sub_sentence_list.append(sentence)
        return sub_sentence_list