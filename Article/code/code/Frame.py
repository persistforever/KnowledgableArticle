# -*- encoding = gb18030 -*-

import codecs
import math
import sys
import numpy as np

import Filter
import Extractor
import Simplifier
from BasicClass import Article


# ---------- Corpus : the processing of corpus ----------
class Corpus :
    # attributes
    artlist = []
    iddict = dict()
    seed = []
    wordbag = dict()
    wordcount = dict()
    idfdict = dict() # word idf dictionary
    traindataset = [] # train dataset
    trainlabel = [] # train label
    testdataset = [] # test data
    testlabel = [] # test label

    # ----- import methods -----
    def importArticle(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [line.strip().split('\t') for line in fo.readlines()]
        for data in datalist :
            article = Article(data)
            self.artlist.append(article)
        self.constrIdDict()
        print 'importing article finished ...'

    def importInfo(self, infopath) :
        with codecs.open(infopath, 'r', 'gb18030') as fo :
            infolist = [line.strip().split('\t') for line in fo.readlines()]
        print 'importing info started ...'
        for data in infolist :
            id = data[0]
            if id in self.iddict :
                self.iddict[id].importInfo(data)
        print 'importing info finished ...'

    def importSplit(self, splitpath) :
        with codecs.open(splitpath, 'r', 'gb18030') as fo :
            splitlist = [line.strip().split('\t') for line in fo.readlines()]
        for data in splitlist :
            id = data[0]
            if id in self.iddict :
                self.iddict[id].importSplit(data)
        print 'importing split finished ...'
    
    def importSplitTitle(self, splitpath) :
        with codecs.open(splitpath, 'r', 'gb18030') as fo :
            splitlist = [line.strip().split('\t') for line in fo.readlines()]
        for data in splitlist :
            id = data[0]
            if id in self.iddict :
                self.iddict[id].importSplitTitle(data)
        print 'importing split finished ...'    
            
    def importLabel(self, labelpath) :
        with codecs.open(labelpath, 'r', 'gb18030') as fo :
            labellist = [line.strip().split('\t') for line in fo.readlines()]
        for data in labellist :
            id = data[0]
            if id in self.iddict :
                self.iddict[id].importLabel(data)
        print 'importing label finished ...'
            
    def importKeyWord(self, keywordpath) :
        with codecs.open(keywordpath, 'r', 'gb18030') as fo :
            keywordlist = [line.strip().split('\t') for line in fo.readlines()]
        for data in keywordlist :
            id = data[0]
            if id in self.iddict :
                self.iddict[id].importKeyWord(data)
        print 'importing keyword finished ...'
            
    def importTrainDataSet(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            data = [np.array(line.strip().split('\t')) for line in fo.readlines()]
        datasetlist = [t[0:-1] for t in data]
        labellist = [t[-1] for t in data]
        self.traindataset = np.array(datasetlist, dtype=float)
        self.traindataset = self.normalization(self.traindataset)
        self.trainlabel = np.array(labellist, dtype=float)
        print 'importing training dataset finished ...'
            
    def importTestDataSet(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            data = [np.array(line.strip().split('\t')) for line in fo.readlines()]
        dataset = [t[1:] for t in data]
        self.testdataset = np.array(dataset, dtype=float)
        self.testdataset = self.normalization(self.testdataset)
        for idx in range(len(data)) :
            id = data[idx][0]
            if id in self.iddict :
                self.iddict[id].importFeatureSet(list(self.testdataset[idx]))
        print 'importing testing dataset finished ...'
        
    def importKnowledgable(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [line.strip() for line in fo.readlines()]
        for id in datalist :
            if id in self.iddict :
                self.iddict[id].label = 1
        print 'importing knowledgable finished ...'
        
    def importSubTitle(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            splitlist = [line.strip().split('\t') for line in fo.readlines()]
        for data in splitlist :
            id = data[0]
            if id in self.iddict :
                self.iddict[id].importSubTitle(data)
        print 'importing subtitle finished ...'
            
    # ----- process methods -----
    def canImport(self, data) :
        if len(data) >= 4 :
            if len(data[0]) > 0 and len(data[1]) > 0 and len(data[2]) > 0 and len(data[3]) > 0 :
                return True
            return False
        
    def constrIdDict(self) :
        self.iddict = dict()
        for article in self.artlist :
            if article.id not in self.iddict :
                self.iddict[article.id] = article

    def filtering(self) :
        print len(self.artlist)
        filter = Filter.CollectionFilter(num=50000)
        self.artlist = filter.filtering(self.artlist)
        print len(self.artlist)
        filter = Filter.ContentLengthFilter(length=500)
        self.artlist = filter.filtering(self.artlist)
        print len(self.artlist)
        # filter = Filter.TimeWordFilter()
        # self.artlist = filter.filtering(self.artlist)
        # print len(self.artlist)
        print 'filtering finished ...'
    
    def selectKeyWord(self) : 
        self.length = len(self.artlist)
        for wordlist in [t.spcontent for t in self.artlist] :
            wordset = set([t.toString() for t in wordlist])
            for word in wordset :
                if word not in self.idfdict.keys() :
                    self.idfdict[word] = 0
                self.idfdict[word] += 1
        for word in self.idfdict :
            self.idfdict[word] = math.log(1.0 * self.length / (self.idfdict[word] + 1), math.e)
        print 'cal IDF value finished ...'
        for article in self.artlist :
            article.calTFIDF(self.idfdict)
            article.selectKeyWord(keywordnum=200)
        print 'selecting keyword finished ...'
    
    def extracting(self) :
        extractor = Extractor.KnowledgableWordExtractor()
        extractor.extractFeature(self.artlist)
        extractor = Extractor.PosExtractor()
        extractor.extractFeature(self.artlist)
        extractor = Extractor.NarrativeExtractor()
        extractor.extractFeature(self.artlist)
        extractor = Extractor.TokenExtractor()
        extractor.extractFeature(self.artlist)
        print 'extracting feature finished ...'

    def constrDataSet(self) :
        self.dataset, self.label = [], []
        for article in self.artlist :
            article.constrFeatureSet()
            self.dataset.append(np.array(article.featureset))
            self.label.append(article.label)
        self.dataset = np.array(self.dataset)
        self.label = np.array(self.label)
        print 'constructing dataset finished ...'
    
    def testClassifier(self) :
        classifier = Classifier.SVMClassifier()
        classifier.comparisonExperiments(self.traindataset, self.trainlabel)
        # classifier.plotDistribution(self.traindataset, 20)
        print 'extracting feature finished ...'

    def normalization(self, dataset) :
        for col in range(dataset.shape[1]) :
            maximum = max(dataset[:, col])
            minimum = min(dataset[:, col])
            for row in range(dataset.shape[0]) :
                if maximum - minimum == 0 :
                    dataset[row, col] = 0.0
                else :
                    dataset[row, col] = 1.0 * (maximum - dataset[row, col]) / (maximum - minimum)
        return dataset
    
    def classifying(self) :
        classifier = Classifier.SVMClassifier()
        clf = classifier.training(self.traindataset[:, :], self.trainlabel)
        # clf = classifier.training(self.traindataset[:, 11:], self.trainlabel)
        print 'training classifier finished ...'
        outartlist = []
        for article in self.artlist :
            if article.label == -1 and article.featureset != [] :
                article.label = classifier.testing(np.array(article.featureset[:]), clf)
                outartlist.append(article)
        sortedlist = list(sorted(outartlist, key=lambda x: x.label[0][1], reverse=True))
        return sortedlist
        print 'extracting feature finished ...'
        
    def titleSpliting(self) :
        simplifier = Simplifier.TitleSimplifier()
        simplifier.splitTitle(self.artlist)
        print 'spliting title finished ...'

    def titleSimplifying(self) :
        artlist = []
        for article in self.artlist :
            if article.label == 1 :
                artlist.append(article)
        simplifier = Simplifier.TitleSimplifier()
        simplifier.simplifying(artlist)
        print 'simpltfying title finished ...'
            
    def contentSpliting(self) :
        simplifier = Simplifier.ContentSimplifier()
        simplifier.splitContent(self.artlist)
        print 'spliting content finished ...'
    
    def paragraphSpliting(self) :
        simplifier = Simplifier.ParagraphSimplifier()
        simplifier.splitParagraph(self.artlist)
        print 'spliting paragraph finished ...'

    # ----- write methods -----
    def writeLine(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.printLine().encode('gb18030') + '\n')
                
    def writeArticle(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.printArticle().encode('gb18030') + '\n')
                
    def writeInfo(self, infopath) :
        with open(infopath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.printInfo().encode('gb18030') + '\n')
                
    def writeSplit(self, splitpath) :
        with open(splitpath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.printSplit().encode('gb18030') + '\n')

    def writeSimplyArticle(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                if article.label == 1 :
                    fw.writelines(article.printSimplyLine().encode('gb18030') + '\n')
                
    def writeKeyWord(self, keywordpath) :
        with open(keywordpath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.id.encode('gb18030')  + '\t' + article.printKeyWord().encode('gb18030') + '\n')
                
    def writeTrainDataSet(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                if article.printLabel() != '-1' :
                    fw.writelines(article.printFeatureSet().encode('gb18030') + article.printLabel().encode('gb18030') + '\n')
                
    def writeTestDataSet(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                if article.printLabel() == '-1' :
                    fw.writelines(article.id.encode('gb18030') + '\t' + article.printFeatureSet().encode('gb18030') + '\n')
                    
    def writeSplitTitle(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                for sub in article.subtitle :
                    fw.writelines(article.id.encode('gb18030') + '\t' + sub.encode('gb18030') + '\n')
                
    def writeSplitContent(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                for sub in article.subcontent :
                    fw.writelines(article.id.encode('gb18030') + '\t' + sub.encode('gb18030') + '\n')
    
    def writeSplitParagraph(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                for sub in article.subparagraph :
                    fw.writelines(article.id.encode('gb18030') + '\t' + sub.encode('gb18030') + '\n')


# ---------- FilePath : list of file path ----------
class FilePath :
    # attributes
    maindir = '/data1/qspace/data/user/hdpfelicialin/cas/gzhzsk/knowledgable/'
    
    # methods
    def getInputArticle(self, type) :
        return self.maindir + 'input/' + type + '/article'
    
    def getInputInfo(self, type) :
        return self.maindir + 'input/' + type + '/info'
    
    def getInputSplit(self, type) :
        return self.maindir + 'input/' + type + '/split'
    
    def getOuputOrigindata(self, type) :
        return self.maindir + 'output/' + type + '/origindata'
    
    def getOutputArticle(self, type) :
        return self.maindir + 'output/' + type + '/article'
    
    def getOutputInfo(self, type) :
        return self.maindir + 'output/' + type + '/info'
    
    def getOutputSplit(self, type) :
        return self.maindir + 'output/' + type + '/split'
    
    def getOutputKeyword(self, type) :
        return self.maindir + 'output/' + type + '/keyword'
    
    def getOutputTestdataset(self, type) :
        return self.maindir + 'output/' + type + '/testdataset'
    
    def getOutputKnowledgablearticle(self, type) :
        return self.maindir + 'output/' + type + '/knowledgablearticle'
    
    def getOutputSubtitle(self, type) :
        return self.maindir + 'output/' + type + '/subtitle'
    
    def getOutputSubcontent(self, type) :
        return self.maindir + 'output/' + type + '/subcontent'
    
    def getOutputSubparagraph(self, type) :
        return self.maindir + 'output/' + type + '/subparagraph'
    
    def getOutputSimplyArticle(self, type) :
        return self.maindir + 'output/' + type + '/simplyknowledgablearticle'
    

# ---------- use collect number to filter ----------
def preFiltering(type) :
    corpus = Corpus()
    filepath = FilePath()
    corpus.importArticle(filepath.getInputArticle(type))
    corpus.importInfo(filepath.getInputInfo(type))
    corpus.importSplitTitle(filepath.getInputSplit(type))
    corpus.filtering()
    corpus.writeLine(filepath.getOuputOrigindata(type))

# ---------- construct dataset ----------
def constrDataSet(type) :
    corpus = Corpus()
    filepath = FilePath()
    corpus.importArticle(filepath.getOutputArticle(type))
    corpus.importSplit(filepath.getOutputSplit(type))
    corpus.importInfo(filepath.getOutputInfo(type))
    corpus.importKeyWord(filepath.getOutputKeyword(type))
    corpus.extracting()
    corpus.constrDataSet()
    corpus.writeTestDataSet(filepath.getOutputTestdataset(type))

# ---------- title spliting ----------
def titleSpliting(type) :
    corpus = Corpus()
    filepath = FilePath()
    corpus.importArticle(filepath.getOutputArticle(type))
    corpus.titleSpliting()
    corpus.writeSplitTitle(filepath.getOutputSubtitle(type))

# ---------- title simplifying ----------
def titleSimplifying(type) :
    corpus = Corpus()
    filepath = FilePath()
    corpus.importArticle(filepath.getOutputArticle(type))
    corpus.importKnowledgable(filepath.getOutputKnowledgablearticle(type))
    corpus.importSubTitle(filepath.getOutputSubtitle(type))
    corpus.importKeyWord(filepath.getOutputKeyword(type))
    corpus.titleSimplifying()
    corpus.writeSimplyArticle(filepath.getOutputSimplyArticle(type))

# ---------- content spliting ----------
def contentSpliting(type) :
    corpus = Corpus()
    filepath = FilePath()
    corpus.importArticle(filepath.getOutputArticle(type))
    corpus.importKnowledgable(filepath.getOutputKnowledgablearticle(type))
    corpus.contentSpliting()
    corpus.writeSplitContent(filepath.getOutputSubcontent(type))
    
# ---------- paragraph spliting ----------
def paragraphSpliting(type) :
    corpus = Corpus()
    filepath = FilePath()
    corpus.importArticle(filepath.getOutputArticle(type))
    corpus.importKnowledgable(filepath.getOutputKnowledgablearticle(type))
    corpus.paragraphSpliting()
    corpus.writeSplitParagraph(filepath.getOutputSubparagraph(type))


# ---------- MAIN ----------
func = sys.argv[1]
type = sys.argv[2]
if func == 'preFiltering' :
    preFiltering(type)
elif func == 'constrDataSet' :
    constrDataSet(type)
elif func == 'titleSpliting' :
    titleSpliting(type)
elif func == 'titleSimplifying' :
    titleSimplifying(type)
elif func == 'contentSpliting' :
    contentSpliting(type)
elif func == 'paragraphSpliting' :
    paragraphSpliting(type)
