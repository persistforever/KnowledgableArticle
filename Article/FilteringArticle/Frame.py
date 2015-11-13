# -*- encoding = gb18030 -*-
import codecs
import numpy as np
import FeatureSelector
import Classifier
import Simplifier
import math
from BasicClass import Article


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
        datasetlist = [t[3:-1] for t in data]
        labellist = [t[-1] for t in data]
        self.traindataset = np.array(datasetlist, dtype=float)
        self.traindataset = self.normalization(self.traindataset)
        self.trainlabel = np.array(labellist, dtype=float)
        print 'importing training dataset finished ...'
            
    def importTestDataSet(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [np.array(line.strip().split('\t')) for line in fo.readlines()]
        dataset = [t[1:] for t in datalist]
        testdataset = np.array(dataset, dtype=float)
        normaltestdataset = self.normalization(testdataset)
        for idx in range(len(datalist)) :
            id = datalist[idx][0]
            if id in self.iddict :
                self.iddict[id].importFeatureSet(list(normaltestdataset[idx]))
                self.iddict[id].importOriginFeatureSet(list(testdataset[idx]))
        print 'importing testing dataset finished ...'
        
    def importKnowledgable(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [line.strip().split('\t') for line in fo.readlines()]
        for data in datalist :
            id = data[0]
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
    def constrIdDict(self) :
        self.iddict = dict()
        for article in self.artlist :
            if article.id not in self.iddict :
                self.iddict[article.id] = article

    def normalization(self, dataset) :
        normaldataset = np.zeros(shape=(dataset.shape[0], dataset.shape[1]))
        for row in range(dataset.shape[0]) :
            for col in range(dataset.shape[1]) :
                normaldataset[row, col] = dataset[row, col]
        for col in range(normaldataset.shape[1]) :
            maximum = max(normaldataset[:, col])
            minimum = min(normaldataset[:, col])
            for row in range(normaldataset.shape[0]) :
                if maximum - minimum == 0 :
                    normaldataset[row, col] = 0.0
                else :
                    normaldataset[row, col] = 1.0 * (maximum - normaldataset[row, col]) / (maximum - minimum)
        return normaldataset
    
    def classifying(self, type) :
        if type == 1 :
            classifier = Classifier.MulticonditionSortingClassifier()
            sortedlist = classifier.processing(self.artlist)
        elif type == 2 :
            classifier = Classifier.SVMClassifier()
            sortedlist = classifier.processing(self.traindataset, self.trainlabel, self.artlist)
        elif type == 3 :
            classifier = Classifier.FeatureSelectedSVMClassifier()
            sortedlist = classifier.processing(self.traindataset, self.trainlabel, self.artlist)
        return sortedlist
        print 'testing classifier finished ...'

    def titleSimplifying(self) :
        artlist = []
        for article in self.artlist :
            if article.label == 1 :
                print article.id
                artlist.append(article)
        simplifier = Simplifier.TitleSimplifier()
        # simplifier.featureSimplifying(artlist)
        simplifier.modelSimplifying(artlist)
        print 'simpltfying title finished ...'
            
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
                
    def writeKeyWord(self, keywordpath) :
        with open(keywordpath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.id.encode('gb18030')  + '\t' + article.printKeyWord().encode('gb18030') + '\n')
                
    def writeTrainDataSet(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                if article.printLabel() != '-1' :
                    fw.writelines(article.id.encode('gb18030') + '\t' + article.printFeatureSet().encode('gb18030') + article.label.encode('gb18030') + '\n')
                
    def writeTestDataSet(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                if article.printLabel() == '-1' :
                    fw.writelines(article.id.encode('gb18030') + '\t' + article.printFeatureSet().encode('gb18030') + '\n')
                    
    def writeSplitTitle(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                if article.label == 1 :
                    for sub in article.subtitle :
                        fw.writelines(article.id.encode('gb18030') + '\t' + sub.encode('gb18030') + '\n')

    def writeSimplyArticle(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                if article.label == 1 :
                    fw.writelines(article.printSimplyLine().encode('gb18030') + '\n')
                
    def writeKnowledgableArticle(self, datapath, artlist, rate=0.1) :
        outnum = int(rate * len(artlist))
        outartlist = artlist[0: outnum]
        with open(datapath, 'w') as fw :
            for article in outartlist :
                fw.writelines(article.printClassifyResult().encode('gb18030') + '\n')


# ---------- FilePath : list of file path ----------
class FilePath :
    # attributes
    maindir = 'E://file/knowledgable/'
    
    # methods
    def getInputArticle(self, type) :
        return self.maindir + 'input/' + type + '/article'
    
    def getInputInfo(self, type) :
        return self.maindir + 'input/' + type + '/info'
    
    def getInputTraindataset(self, type) :
        return self.maindir + 'input/' + type + '/traindataset'
    
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
    
    def getOutputSimplyArticle(self, type) :
        return self.maindir + 'output/' + type + '/simplyknowledgablearticle'

    def getOutputSimilarity(self, type) :
        return self.maindir + 'output/' + type + '/featuresimilarity'
        

# ---------- classifying ----------
def classifying(type) :
    corpus = Corpus()
    filepath = FilePath()
    corpus.importTrainDataSet(filepath.getInputTraindataset(type))
    corpus.importArticle(filepath.getOutputArticle(type))
    corpus.importTestDataSet(filepath.getOutputTestdataset(type))
    sortedlist = corpus.classifying(2)
    corpus.writeKnowledgableArticle(filepath.getOutputKnowledgablearticle(type), sortedlist, rate=0.2)

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


# ---------- MAIN ----------
type = '4/20150704'
classifying(type)
titleSimplifying(type)