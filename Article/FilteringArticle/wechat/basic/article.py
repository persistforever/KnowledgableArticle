# -*- encoding = gb18030 -*-

# package importing start
import numpy as np

from word import Word
# package importing end


class Article :

    def __init__(self) :
        self.split_title = []
        self.split_content = []
        self.sub_title = []
        self.sub_sentence_list = []
        self.keyword_list = []
        self.feature_set = []

    def set_params(self, **params) :
        """ Set parameters of the article. """
        for key, value in params.iteritems() :
            setattr(self, key, value)

    def set_attributes(self, *params) :
        """ Set attributes of the article. """
        for cmd in params :
            key, value = cmd.split('<=>')
            setattr(self, key, value)

    def set_features(self, **params) :
        """ Set features of the article. """
        for key, value in params.iteritems() :
            self.feature_set.append((key, float(value)))

    def import_split(self, data) :
        """ Import word splited title and content. 
        The attributes of split is 
        [id, split_title, split_content]. """
        self.split_title, self.split_content = [], []
        for part in data[1].split(' ') :
            word = Word(part, sp_char=':')
            self.split_title.append(word)
        for part in data[2].split(' ') :
            word = Word(part, sp_char=':')
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
        self.sub_sentence_list.append(sub)
    
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