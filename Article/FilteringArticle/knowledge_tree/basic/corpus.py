# -*- encoding = gb18030 -*-

# package importing start
import numpy as np

from article import Article
from article import Word
from file.file_operator import BaseFileOperator, CSVFileOperator, TextFileOperator
# package importing end



class Corpus(object) :

    def __init__(self) :
        pass

    def article_info(self, article_path, type='load') :
        """ If type == 'create' : 
                Create article info after simplifying.
            If type == 'load' : 
                Read article list.
                Each row of the file is a article.
                column[0] of the file is the id of article.
                column[1] of the file is the url of article.
                column[2] of the file is the title of article.
                column[3] of the file is the content of article.
        """
        file_operator = TextFileOperator()
        if type == 'create' :
            data_list = []
            entry_list = ['id', 'url', 'title', 'content']
            data_list.append(entry_list)
            for article in self.article_list :
                data = []
                for idx, key in enumerate(entry_list) :
                    data.append(article[key])
                data_list.append(data)
            file_operator.writing(data_list, article_path)
        elif type == 'load' :
            data_list = file_operator.reading(article_path)
            entry_list = data_list[0]
            self.article_list = []
            for data in data_list[1:] :
                if len(data) >= len(entry_list) :
                    article = dict()
                    for idx, key in enumerate(entry_list) :
                        article[key] = data[idx]
                    self.article_list.append(article)
            self._constr_id_article_dict()
            self._constr_id_index_dict()

    def participle_list(self, split_path, type='load', target='participle_title') :
        """ If type == 'load' :
                Read participle title list.
                Each row of the file is a article.
                column[0] of the file is the id of article.
                column[1] of the file is the participle_title of article.
        """
        file_operator = TextFileOperator()
        if type == 'load' :
            data_list = file_operator.reading(split_path)
            entry_list = data_list[0]
            for data in data_list[1:] :
                if len(data) >= len(entry_list) :
                    id = data[0]
                    if id in self._id_article_dict :
                        self._id_article_dict[id][target] = \
                            [Word(part, sp_char=':') for part in data[1].split(' ')]

    def segemented_list(self, sentence_path, type='create', target='title', \
        segementor=None) :
        """ If type == 'create' : 
                Create sub sentences list from article.
                using simplifier to split article title or content into sub sentences.
            If type == 'load' : 
                Each row of the file is a sentence.
                column[0] of the file is the id of article.
                column[1] of the file is the sub_sentence of article.
        """
        file_operator = TextFileOperator()
        if type == 'create' :
            data_list = []
            entry_list = ['id', 'segemented_'+target]
            data_list.append(entry_list)
            for article in self.article_list :
                sentence = article[target]
                segemented_sentence = segementor.segement(sentence)
                for sentence in segemented_sentence :
                    data_list.append([article['id'], sentence])
            file_operator.writing(data_list, sentence_path)
        elif type == 'load' :
            data_list = file_operator.reading(sentence_path)
            entry_list = data_list[0]
            for article in self.article_list :
                article['segemented_'+target] = []
            for data in data_list[1:] :
                if len(data) >= len(entry_list) :
                    id = data[0]
                    if id in self._id_article_dict :
                        if 'segemented_'+target in self._id_article_dict[id].keys() :
                            self._id_article_dict[id]['segemented_'+target].append(data[1])

    def segemented_participle_list(self, sentence_path, type='create', target='title') :
        """ If type == 'create' : 
                Create sub sentences list from article.
                using simplifier to split article title or content into sub sentences.
            If type == 'load' : 
                Each row of the file is a sentence.
                column[0] of the file is the id of article.
                column[1] of the file is the sub_sentence of article.
        """
        file_operator = TextFileOperator()
        if type == 'create' :
            data_list = []
            entry_list = ['id', 'segemented_'+target]
            data_list.append(entry_list)
            for article in self.article_list :
                sentence = article[target]
                segemented_sentence = segementor.segement(sentence)
                for sentence in segemented_sentence :
                    data_list.append([article['id'], sentence])
            file_operator.writing(data_list, sentence_path)
        elif type == 'load' :
            data_list = file_operator.reading(sentence_path)
            entry_list = data_list[0]
            for article in self.article_list :
                article['segemented_participle_'+target] = []
            for data in data_list[1:] :
                if len(data) >= len(entry_list) :
                    id = data[0]
                    if id in self._id_article_dict :
                        if 'segemented_participle_'+target in self._id_article_dict[id].keys() :
                            self._id_article_dict[id]['segemented_participle_'+target].append( \
                                [Word(part, sp_char=':') for part in data[1].split(' ')])

    def _constr_id_article_dict(self) :
        """ Construct id_article dict.
        key is id, value is Article object. """
        self._id_article_dict = dict()
        for article in self.article_list :
            self._id_article_dict[article['id']] = article
        print 'constructing _id_article dict finished ...'

    def _constr_id_index_dict(self) :
        """ Construct id_index dict of article.
        key is id, value is index object. """
        self._id_index_dict = dict()
        for index, article in enumerate(self.article_list) :
            self._id_index_dict[article['id']] = index
        print 'constructing _id_index dict finished ...'

    def simplify_content(self, simplifier=None) :
        """ Simplify content. """
        target = 'content'
        for idx, article in enumerate(self.article_list) :
            sentence_list = []
            for sentence in article['segemented_'+target] :
                sentence_list.append(simplifier.tag_sentence(sentence))
            sentence_list = simplifier.filter_tail(sentence_list)
            sentence_list = simplifier.filter_head(sentence_list)
            article[target] = ''
            for sentence, flag in sentence_list :
                article[target] += sentence + u'。'

    def simplify_title(self, dictionary, texts, tfidf, simplifier=None) :
        """ Simplify title. """
        target = 'title'
        for idx, article in enumerate(self.article_list) :
            sentences = []
            for sentence in article['segemented_participle_'+target] :
                sentences.append([word for word in sentence])
            words = [dictionary[word] for word, value in \
                sorted(tfidf[texts[idx]], key=lambda x: x[1], reverse=True)[0:10]]
            sentence = simplifier.filter_sentence(sentences, words)
            article[target] = ''.join([word.name for word in sentence])

    def simplify_article(self) :
        """ Unique article. """
        article_list = []
        title_dict = dict()
        for idx, article in enumerate(self.article_list) :
            if article['title'] not in title_dict :
                title_dict[article['title']] = None
                article_list.append(article)
        self.article_list = article_list

    def article_to_texts(self, target='participle_title') :
        """ Transform article to texts accordding to gensim. 
            Texts is a [list] and each element is a [list].
            Each element of the texts_list is a article.
            Each element of the article is a word.
            Like this [ [word_a, word_b, ...], 
                        [word_c, word_d, ...], 
                        ...
                      ]
        """
        remain_pos = [u'vn', u'nz', u'nt', u'ns', u'n', u'an']
        texts = []
        for article in self.article_list :
            text = []
            if target in article.keys() :
                text.extend([word.to_string() for word in article[target] if word.feature in remain_pos])
            texts.append(text)
        return texts
    
    def article_to_sentences(self, target='segemented_participle_title') :
        """ Transform article to sentences accordding to gensim. 
            Sentences is a [list] and each element is a [list].
            Each element of the Sentences is a sentence.
            Each element of the sentence is a word.
            Like this [ [word_a, word_b, ...], 
                        [word_c, word_d, ...], 
                        ...
                      ]
        """
        sentences = []
        for article in self.article_list :
            for sentence in article[target] :
                if len(sentence) > 5 :
                    sentences.append([word.to_string() for word in sentence])
        return sentences