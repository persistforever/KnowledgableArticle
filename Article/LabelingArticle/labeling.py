# -*- encoding = gbk -*-
'''
Class Corpus : labeling article
    label meaning : 1-knowledgable, 0-unknowledgable, -1-unknown
'''

import wx
import codecs
from BasicClass import Article
from BasicClass import Conf


class Corpus :
    # ----- attributes -----
    artlist = []
    ukllist = []
    uklist = []
    kllist = []

    # ----- import methods -----
    def importArticle(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [line.strip().split('\t') for line in fo.readlines()[0:100]]
        for data in datalist :
            article = Article(data)
            self.artlist.append(article)
        self.constrIdDict()

    def importLabel(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [line.strip().split('\t') for line in fo.readlines()]
        for data in datalist :
            id = data[0]
            if id in self.iddict :
                self.iddict[id].importLabel(data)

    # ----- process methods -----
    def constrIdDict(self) :
        self.iddict = dict()
        for article in self.artlist :
            if article.id not in self.iddict :
                self.iddict[article.id] = article
    
    # ----- write methods -----
    def writeLabel(self, labelpath) :
        with open(labelpath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.id.encode('gb18030') + '\t' + str(article.label).encode('gb18030') + '\n')


class StaticTextFrame(wx.Frame):  
    def __init__(self):  
        self.corpus = Corpus()
        self.corpus.importArticle('E://file/knowledgable/labeling/article')
        self.corpus.importLabel('E://file/knowledgable/labeling/label')
        self.conf = Conf()
        [self.idx] = self.conf.readConf()
        self.title = self.corpus.artlist[self.idx].title
        self.url = self.corpus.artlist[self.idx].url
        self.corpus.ukllist, self.corpus.uklist, self.corpus.kllist = [], [], []
        wx.Frame.__init__(self, None, -1, 'labeling', size=(1000, 350))
        self.panel = wx.Panel(self, -1)
        self.constrFrame()

    def constrFrame(self) :
        # title
        self.titletext = wx.StaticText(self.panel, -1, self.title, pos=(50, 20), size=(900, 50), style=wx.ALIGN_CENTER)
        self.titletext.SetBackgroundColour(wx.Colour(232,232,255))
        self.titletext.SetForegroundColour(wx.Colour(0,0,0))
        font = wx.Font(18, wx.FONTFAMILY_TELETYPE, wx.FONTWEIGHT_NORMAL, wx.NORMAL)
        self.titletext.SetFont(font)
        self.titletext.SetSize((900, 30))
        # content
        self.contenttext = wx.HyperlinkCtrl(self.panel, -1, self.url, self.url, pos=(50, 70), size=(900, 50), style=wx.ALIGN_CENTER)
        self.contenttext.SetBackgroundColour(wx.Colour(232,232,255))
        self.contenttext.SetForegroundColour(wx.Colour(0,0,0))
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.NORMAL)
        self.contenttext.SetFont(font)
        self.contenttext.SetSize((900, 50))
        # page
        self.pagetext = wx.StaticText(self.panel, -1, str(self.idx)+'/'+str(len(self.corpus.artlist)), pos=(375, 230), size=(250, 30), style=wx.ALIGN_CENTER)
        self.pagetext.SetBackgroundColour(wx.Colour(232,232,255))
        self.pagetext.SetForegroundColour(wx.Colour(0,0,0))
        font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.NORMAL)
        self.pagetext.SetFont(font)
        self.pagetext.SetSize((250, 30))
        # button
        goodbutton = wx.Button(self.panel, label=u'knowledgeable', pos=(50, 150), size=(250, 50))
        goodbutton.Bind(wx.EVT_BUTTON, self.markGood, goodbutton)
        badbutton = wx.Button(self.panel, label=u'unknowledgeable', pos=(375, 150), size=(250, 50))
        badbutton.Bind(wx.EVT_BUTTON, self.markBad, badbutton)
        unknowbutton = wx.Button(self.panel, label=u'unknow', pos=(700, 150), size=(250, 50))
        unknowbutton.Bind(wx.EVT_BUTTON, self.markUnknow, unknowbutton)
        upperbutton = wx.Button(self.panel, label=u'nextpage', pos=(50, 230), size=(250, 50))
        upperbutton.Bind(wx.EVT_BUTTON, self.frontPage, upperbutton)
        savebutton = wx.Button(self.panel, label=u'save', pos=(700, 230), size=(250, 50))
        savebutton.Bind(wx.EVT_BUTTON, self.save, savebutton)

    def markGood(self, event):
        self.corpus.artlist[self.idx].label = 1
        self.corpus.kllist.append(self.corpus.artlist[self.idx])
        if self.idx < len(self.corpus.artlist)-1 :
            self.idx += 1
        self.title = self.corpus.artlist[self.idx].title
        self.url = self.corpus.artlist[self.idx].url
        self.titletext.SetLabel(self.title)
        self.titletext.SetSize((900, 30))
        self.contenttext.SetLabel(self.url)
        self.contenttext.SetURL(self.url)
        self.contenttext.SetSize((900, 30))
        self.pagetext.SetLabel(str(self.idx)+'/'+str(len(self.corpus.artlist)))
        self.pagetext.SetSize((250, 30))

    def markBad(self, event): 
        self.corpus.artlist[self.idx].label = 0
        self.corpus.ukllist.append(self.corpus.artlist[self.idx])
        if self.idx < len(self.corpus.artlist)-1 :
            self.idx += 1
        self.title = self.corpus.artlist[self.idx].title
        self.url = self.corpus.artlist[self.idx].url
        self.titletext.SetLabel(self.title)
        self.titletext.SetSize((900, 30))
        self.contenttext.SetLabel(self.url)
        self.contenttext.SetURL(self.url)
        self.contenttext.SetSize((900, 30))
        self.pagetext.SetLabel(str(self.idx)+'/'+str(len(self.corpus.artlist)))
        self.pagetext.SetSize((250, 30))

    def markUnknow(self, event):
        self.corpus.artlist[self.idx].label = -1
        self.corpus.uklist.append(self.corpus.artlist[self.idx])
        if self.idx < len(self.corpus.artlist)-1 :
            self.idx += 1
        self.title = self.corpus.artlist[self.idx].title
        self.url = self.corpus.artlist[self.idx].url
        self.titletext.SetLabel(self.title)
        self.titletext.SetSize((900, 30))
        self.contenttext.SetLabel(self.url)
        self.contenttext.SetURL(self.url)
        self.contenttext.SetSize((900, 30))
        self.pagetext.SetLabel(str(self.idx)+'/'+str(len(self.corpus.artlist)))
        self.pagetext.SetSize((250, 30))

    def frontPage(self, event):
        if self.idx > 0 :
            self.idx -= 1
        self.title = self.corpus.artlist[self.idx].title
        self.url = self.corpus.artlist[self.idx].url
        self.titletext.SetLabel(self.title)
        self.titletext.SetSize((900, 30))
        self.contenttext.SetLabel(self.url)
        self.contenttext.SetURL(self.url)
        self.contenttext.SetSize((900, 30))
        self.pagetext.SetLabel(str(self.idx)+'/'+str(len(self.corpus.artlist)))
        self.pagetext.SetSize((250, 30))

    def save(self, event):
        self.conf.writeConf([self.idx])
        self.corpus.writeLabel('E://file/knowledgable/labeling/label')
        print 'already save'


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = StaticTextFrame()
    frame.Show()
    app.MainLoop()