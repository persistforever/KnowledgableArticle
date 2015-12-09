# -*- encoding = gb18030 -*-

# package importing start
import re

from basic.corpus import Corpus
from file.file_operator import TextFileOperator
# package importing end


class SentenceSpliter :

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


class AnotherCorpus(Corpus) :

    def __init__(self) :
        super(AnotherCorpus, self).__init__()

    def read_article_list(self, article_path):
        return super(AnotherCorpus, self).read_article_list(article_path)

    def content_split_sentence(self, spst_path) :
        """ Split content as sub_sentence_list. """
        spliter = SentenceSpliter(spst_path=spst_path)
        for article in self.article_list :
            article.sub_sentence_list = spliter.split_content(article.content)

    def write_content_sentence_list(self, sentence_path) :
        """ Write splited sentence.
            Each row of the file is a splited sentence.
            Column[0] of the file is article id.
            Column[1] of the file is the splited sentence.
        """
        file_operator = TextFileOperator()
        data_list = [['id', 'sentence']]
        for article in self.article_list :
            for sentence in article.sub_sentence_list :
                data = [article.id, sentence]
                data_list.append(data)
        file_operator.writing(data_list, sentence_path)