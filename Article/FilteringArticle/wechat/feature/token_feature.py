# -*- encoding = gb18030 -*-

# package importing start
import re 

from file.file_operator import TextFileOperator
from feature.base import BaseExtractor
# package importing end


class TokenExtractor(BaseExtractor) :
    
    def __init__(self, sp_path='', pc_path='') :
        BaseExtractor.__init__(self)

        self.split_dict = self._read_dictionary(sp_path)
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
    
    def extractFeature(self, article_list) :
        for article in article_list :
            title_length = len(article.title)
            content_length = len(article.content)
            n_title_word = len(article.split_title) 
            n_content_word = len(article.split_content)
            titleword_dict = dict()
            for word in article.split_title :
                if word.name not in titleword_dict :
                    titleword_dict[word.name] = None
            contentword_dict = dict()
            for word in article.split_content :
                if word.name not in contentword_dict :
                    contentword_dict[word.name] = None
            n_dist_title_word = len(titleword_dict)
            n_dist_content_word = len(contentword_dict)
            n_title_punc = len([char for char in article.title if char in self.punc_dict])
            n_content_punc = len([char for char in article.content if char in self.punc_dict])
            paragraph_split_char = '[\u3000]'
            paragraph_list = re.split(paragraph_split_char, article.content)
            n_paragraph = len(paragraph_list)
            sentence_split_char = '['
            for sp in self.split_dict :
                sentence_split_char += sp + '|'
            sentence_split_char += ']'
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
            article.set_features(title_length=title_length, content_length=content_length, \
                n_title_word=n_title_word, n_content_word=n_content_word, \
                n_dist_title_word=n_dist_title_word, n_dist_content_word=n_dist_content_word, \
                n_title_punc=n_title_punc, n_content_punc=n_content_punc, n_paragraph=n_paragraph, \
                n_sentence=n_sentence, avg_sentence_lenght=avg_sentence_lenght, \
                avg_paragraph_lenght=avg_paragraph_lenght)
