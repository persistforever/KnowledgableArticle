# -*- encoding = utf8 -*-
'''
topic model
'''

import codecs
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
                
    # ----- process methods -----
    def constrTree(self, bagofword) :
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
        for data in bagofword :
            s = sum(data)
            if s == 0 :
                print 'fuck!'
    
    def process(self) :
        '''
        worddict2 = self.importWordIDF('E:\\download\\2_idf')
        worddict4 = self.importWordIDF('E:\\download\\4_idf')
        worddict5 = self.importWordIDF('E:\\download\\5_idf')
        worddict6 = self.importWordIDF('E:\\download\\6_idf')
        wordlist = self.compare(worddict4, [worddict2, worddict5, worddict6])
        self.writeKeyWord('E:\\download\\cmpidf', wordlist)
        '''
        bagofword = self.importBOW('E:\\download\\bagofword')
        self.existRepeat(bagofword)
        wordlist = self.constrTree(bagofword)
        self.writeWordTopic('E:\\download\\wordtopic.csv', wordlist)

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


model = LDA()
model.process()
