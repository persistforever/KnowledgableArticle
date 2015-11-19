# -*- encoding = utf8 -*-
'''
tag article
'''

import codecs
import math
import numpy as np
import lda
import os
import csv
from Basic import Article


class Tag :
    # ----- init method -----
    def __init__(self) :
        self.artlist = []
        self.artdict = dict()

    # ----- import methods -----
    def importArticle(self, datapath) :
        with codecs.open(datapath, 'rb', 'gb18030') as fo :
            csvreader = csv.reader(fo)
            for data in csvreader :
                if len(data) >= 1 :
                    article = Article.Article(id=data[0])
                    self.artlist.append(article)
        print 'importing article finished ...'

    def importBOW(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [line.strip().split('\t') for line in fo.readlines()]
        for data in datalist :
            if len(data) >= 2 :
                if data[0] in self.artdict :
                    self.artdict[data[0]].bowvector = np.array(data[1].split(' '), dtype=int)
        print 'importing bagofword finished ...'

    def importWordSet(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [line.strip().split('\t') for line in fo.readlines()]
        self.wordindex, self.indexword = dict(), dict()
        for data in datalist :
            if len(data) >= 2 :
                if data[0] not in self.wordindex :
                    self.wordindex[data[0]] = int(data[1])
                    self.indexword[int(data[1])] = data[0]
        print 'importing wordset finished ...'
                
    # ----- process methods -----
    def constrArticleDict(self) :
        for article in self.artlist :
            if article.id not in self.artdict :
                self.artdict[article.id] = article
        print 'constructing articledict finished ...'

    def constrIdIndexDict(self) :
        self.idindex, self.indexid = dict(), dict()
        for index, id in enumerate(self.artdict) :
            self.idindex[id] = index
            self.indexid[index] = id
        print 'constructing idindexdict finished ...'

    def constrSubTree(self, condidatearticle) :
        if len(condidatearticle) <= 1 :
            return condidatearticle, True
        bagofword = []
        for article in condidatearticle :
            bagofword.append(article.bowvector)
        bagofword = np.array(bagofword)
        for x in range(bagofword.shape[0]) :
            for y in range(bagofword.shape[1]) :
                if bagofword[x, y] != 0 :
                    bagofword[x, y] = 1
        wordetp = []
        N = bagofword.shape[0]
        for idx in range(bagofword.shape[1]) :
            p = 1.0 * sum(bagofword[:, idx].tolist()) / N
            if p == 0.0 :
                etp = 0.0
            else :
                etp = - p * math.log(p)
            wordetp.append([idx, etp, p])
        wordetp = sorted(wordetp, key=lambda x: x[1], reverse = True)
        wordidx = 0
        for idx, etp, p in wordetp :
            if len(self.indexword[idx+1].split(':')) == 2 :
                if self.indexword[idx+1].split(':')[1] in [u'n'] :
                    wordidx = idx
                    print idx+1, self.indexword[idx+1].encode('gb18030'), etp, p*N
                    break
        choosed = int(raw_input('is it raleted to ' + self.indexword[wordidx+1] + '? '))
        condidate = []
        for article in condidatearticle :
            exist = 0
            if article.bowvector[wordidx] != 0 :
                exist = 1
            if exist == choosed :
                condidate.append(article)
        print condidate
        return condidate, False
    
    def process(self) :
        self.importArticle(os.path.abspath('E://file/knowledgable/lucene/output/queryresult.csv'))
        self.constrArticleDict()
        self.constrIdIndexDict
        self.importBOW(os.path.abspath('E://file/knowledgable/input/4/bagofword'))
        self.importWordSet(os.path.abspath('E://file/knowledgable/input/4/wordset'))
        condidatearticle, stop = self.constrSubTree(self.artlist)
        while stop == False :
            print condidatearticle[0].id
            condidatearticle, stop = self.constrSubTree(condidatearticle)

    # ----- write methods -----
    def writeKeyWord(self, datapath, wordlist) :
        with open(datapath, 'w') as fw :
            for word, score in wordlist :
                fw.writelines(word.encode('gb18030') + '\t' + str(score).encode('gb18030') + '\n')

    def writeWordTopic(self, datapath, wordlist) :
        with open(datapath, 'wb') as fw :
            csvfile = csv.writer(fw)
            for word in wordlist :
                csvfile.writerow(word)


tag = Tag()
tag.process()
