# -*- encoding = gb18030 -*-
""" Simplify the title. """

import codecs
import numpy as np
import re
import gensim
from basic.article import Article
from file.path_manager import PathManager
from file.file_operator import TextFileOperator


class TitleSimplifier :
    # attributes
    spdict = dict()
    
    # methods    
    def __init__(self) :
        self.path_manager = PathManager()
        self.spdict = self.importSpDict()
        self.vecmodel = gensim.models.Word2Vec.load(self.path_manager.get_tools_vector())
        
    def importSpDict(self) :
        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_tools_titlespst())
        spdict = dict()
        for data in data_list :
            if len(data) >= 1 :
                if data[0] not in spdict :
                    spdict[data[0]] = None
        return spdict

    def splitSentence(self, article, splitchar) :
        sentenceset = re.split(splitchar, article.title)
        return sentenceset

    def featureSentenceScore(self, sentence, keyword) :
        top = 0
        bottem = len(sentence) + len(keyword)
        stc = ''
        keyline = ''
        for word in keyword :
            keyline += word.name
        for word in sentence :
            stc += word.name
            for char in word.name :
                if char in keyline :
                    top += 1
                    break
        score = 1.0 * top / bottem + len([1 for t in sentence if t.feature == 'n']) * 0.01 + len(sentence) * 0.01
        return [stc, score]
    
    def model_sentence_score(self, sentence, keyword) :
        stc = ''
        score = 0.0
        for worda in sentence :
            stc += worda.name
            for wordb in keyword :
                try:
                    score += self.vecmodel.similarity( \
                        worda.name.encode('utf8'), wordb.name.encode('utf8'))
                except Exception, e:
                    pass
        return [stc, score]

    def splitTitle(self, artlist) :
        splitchar = '[\[\]\|?'
        for sp in self.spdict :
            splitchar += sp
        splitchar += ' ]'
        for article in artlist :
            sentenceset = self.splitSentence(article, splitchar)
            article.subtitle = []
            for sentence in sentenceset :
                if sentence.strip() != '' :
                    article.subtitle.append(sentence)
                    
    def featureSimplifying(self, artlist) :
        for article in artlist :
            sentencelist = []
            for sentence in article.subtitle :
                sentencescore = self.featureSentenceScore(sentence, [t[0] for t in article.keyword[0:20]])
                sentencelist.append(sentencescore)
            sentencelist = sorted(sentencelist, key=lambda x: x[1], reverse=True)
            article.simplytitle = sentencelist[0][0]
                    
    def model_simplifying(self, artlist) :
        for article in artlist :
            sentencelist = []
            for sentence in article.sub_title :
                sentencescore = self.model_sentence_score(sentence, \
                    [t[0] for t in article.keyword_list[0:20]])
                sentencelist.append(sentencescore)
            sentencelist = sorted(sentencelist, key=lambda x: x[1], reverse=True)
            article.simply_title = sentencelist[0][0]
