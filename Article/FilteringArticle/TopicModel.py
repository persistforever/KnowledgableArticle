# -*- encoding = utf8 -*-
'''
topic model
'''

import codecs
import math
import numpy as np
import lda
import csv
from BasicClass import Article


class LDA :
    # ----- import methods -----
    def importWordIDF(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [line.strip().split('\t') for line in fo.readlines()]
        worddict = dict()
        for data in datalist :
            if len(data) >= 2 :
                if data[0] not in worddict :
                    worddict[data[0]] = float(data[1])
        print 'importing wordidf finished ...'
        return worddict

    def importBOW(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [line.strip().split('\t') for line in fo.readlines()]
        bagofword = []
        for data in datalist :
            if len(data) >= 2 :
                bagofword.append(np.array(data[1].split(' '), dtype=int))
        print 'importing bagofword finished ...'
        return np.array(bagofword)

    def importWordSet(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [line.strip().split('\t') for line in fo.readlines()]
        wordindex = dict()
        indexword = dict()
        for data in datalist :
            if len(data) >= 2 :
                if data[0] not in wordindex :
                    wordindex[data[0]] = int(data[1])
                    indexword[int(data[1])] = data[0]
        print 'importing worddict finished ...'
        return wordindex, indexword
                
    # ----- process methods -----
    def constrLDA(self, bagofword) :
        model = lda.LDA(n_topics=10, n_iter=500, random_state=1).fit(bagofword)
        wordlist = []
        for idx in range(model.topic_word_.shape[1]) :
            wordlist.append(model.topic_word_[:, idx].transpose().tolist())
        return wordlist

    def compare(self, worddict, cmpdictlist) :
        wordlist = []
        for word in worddict :
            dictnum = 0
            score = 1
            for cmpdict in cmpdictlist :
                if word in cmpdict :
                    dictnum += 1
                    score *= (cmpdict[word] + 1) / (worddict[word] + 1)
            if dictnum != 0 :
                wordlist.append([word, 1.0*score/dictnum])
        wordlist = sorted(wordlist, key=lambda x: x[1], reverse=True)
        return wordlist

    def existRepeat(self, bagofword) :
        num = 0
        for data in bagofword :
            s = sum(data)
            if s == 0 :
                num += 1
        print num

    def constrSubTree(self, bagofword, indexword, level) :
        wordetp = []
        N = bagofword.shape[0]
        if level >= 4 :
            return
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
            if len(indexword[idx+1].split(':')) == 2 :
                if indexword[idx+1].split(':')[1] in [u'n'] :
                    wordidx = idx
                    print idx+1, indexword[idx+1].encode('gb18030'), etp, p, level
                    break
        posibow, negabow = [], []
        for i in range(bagofword.shape[0]) :
            if bagofword[i, wordidx] == 0 :
                negabow.append(bagofword[i, :])
            else :
                posibow.append(bagofword[i, :])
        self.constrSubTree(np.array(posibow), indexword, level+1)
        self.constrSubTree(np.array(negabow), indexword, level+1)
    
    def process(self) :
        worddict2 = self.importWordIDF('E:\\download\\2_idf')
        worddict4 = self.importWordIDF('E:\\download\\4_idf')
        worddict5 = self.importWordIDF('E:\\download\\5_idf')
        worddict6 = self.importWordIDF('E:\\download\\6_idf')
        wordlist = self.compare(worddict2, [worddict4, worddict5, worddict6])
        self.writeKeyWord('E:\\download\\cmpidf', wordlist)
        '''
        bagofword = self.importBOW('E:\\download\\bagofword')
        wordindex, indexword = self.importWordSet('E:\\download\\wordset') 
        for x in range(bagofword.shape[0]) :
            for y in range(bagofword.shape[1]) :
                if bagofword[x, y] != 0 :
                    bagofword[x, y] = 1
        #self.existRepeat(bagofword)
        self.constrSubTree(bagofword, indexword, 0)
        #wordlist = self.constrTree(bagofword)
        #self.writeWordTopic('E:\\download\\wordtopic.csv', wordlist)
        '''

    # ----- write methods -----
    def writeKeyWord(self, datapath, wordlist) :
        with open(datapath, 'w') as fw :
            index = 1
            for word, score in wordlist[0:5000] :
                fw.writelines(word.encode('gb18030') + '\t' + str(index).encode('gb18030') + '\n')
                index += 1

    def writeWordTopic(self, datapath, wordlist) :
        with open(datapath, 'wb') as fw :
            csvfile = csv.writer(fw)
            for word in wordlist :
                csvfile.writerow(word)


model = LDA()
model.process()
