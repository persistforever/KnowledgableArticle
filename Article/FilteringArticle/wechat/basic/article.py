# -*- encoding = gb18030 -*-
""" Class article """

from word import Word
import numpy as np


class Article :

    def __init__(self) :
        self.split_title = []
        self.split_content = []
        self.sub_title = []
        self.sub_sentence = []

    def set_params(self, **params) :
        """ Set parameters of the article. """
        for key, value in params.iteritems() :
            setattr(self, key, value)

    def import_article(self, data) :
        """ Import basic attributes of article. 
        The attributes of article is [id, url, title, content]. """
        self.id = data[0]
        self.url = data[1]
        self.title = data[2]
        self.content = data[3]
                
    def import_info(self, data) :
        """ Import infomation of article. 
        The attributes of info is 
        [id, time_pub, n_forward, n_zan, n_click, n_collect, time_read, finish_ratio]. """
        self.time_pub = int(data[1])
        self.n_forward = int(data[2])
        self.n_zan = int(data[3])
        self.n_click = int(data[4])
        self.n_collect = int(data[5])
        self.time_read = float(data[6])
        self.finish_ratio = float(data[7])

    def import_split(self, data) :
        """ Import word splited title and content. 
        The attributes of split is 
        [id, split_title, split_content]. """
        self.split_title, self.split_content = [], []
        for part in data[1].split(' ') :
            word = Word(part)
            self.split_title.append(word)
        for part in data[2].split(' ') :
            word = Word(part)
            self.split_content.append(word)
            
    def import_keyword(self, data, length=100) :
        """ Import key words(highest tf-idf) of the content. 
        The attributes of keyword is 
        [id, keyword]. """
        self.keyword_list = []
        for part in data[1:length+1] :
            word = Word(part.split('<#>')[0])
            tfidf = float(part.split('<#>')[1])
            self.keyword_list.append([word, tfidf])
            
    def import_feature_set(self, data) :
        """ Import feature set of article. 
        The attributes of feature set is 42 attributes divided in 4 levels.
        [id, token_level, user_level, word_level, pos_level]. """
        self.feature_set = []
        for value in data :
            self.feature_set.append(float(value))
            
    def import_bagofword(self, data) :
        """ Import bagofword vector of article. 
        The entry of vecotr is N words. """
        self.bagofword_vector = []
        for value in data :
            self.bagofword_vector.append(int(value))
        self.bagofword_vector = np.array(self.bagofword_vector)

    def import_sub_title(self, data) :
        """ Import sub title of article. """
        sub = []
        for part in data[1].split(' ') :
            word = Word(part, sp_char=':')
            sub.append(word)
        self.sub_title.append(sub)

    def import_sub_sentence(self, data) :
        """ Import sub sentence of article. """
        sub = []
        for part in data[1].split(' ') :
            word = Word(part, sp_char=':')
            sub.append(word)
        self.sub_sentence.append(sub)
    
    def get_article(self) :
        """ get basic attributes of article. 
        The attributes of article is [id, url, title, content]. """
        line = []
        line.append(self.id)
        line.append(self.url)
        line.append(self.title)
        line.append(self.content)
        return line
    
    def get_tag_list(self) :
        """ get tag list of article. """
        line = []
        line.append(self.id)
        tagstr = ''
        for tag in self.tag_list :
            tagstr += str(tag) + ' '
        line.append(tagstr.strip())
        return line

    def get_feature_set(self) :
        """ get feature set of article. """
        line = []
        for feature in self.feature_set :
            line.append(str(feature))
        return line

    def get_simply_article(self) :
        """ get simply title and other attributes of article. """
        line = []
        line.append(self.id)
        line.append(self.url)
        line.append(self.simply_title)
        line.append(self.content)
        return line