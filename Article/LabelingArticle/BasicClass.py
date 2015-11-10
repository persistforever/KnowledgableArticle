# -*- encoding = gb18030 -*-
'''
Class Conf : read and write configuration
Class Word : struction of word
Class Article : struction of article
'''
import codecs
import ConfigParser
import math


class Conf :
    # ----- attributes ----- 
    filename = 'E://file/knowledgable/labeling/settings.ini'

    # ----- methods -----
    def readConf(self) :
        arr = []
        cf = ConfigParser.ConfigParser()
        cf.read(self.filename)
        arr.append(int(cf.get('article', 'startidx')))
        return arr

    def writeConf(self, arr) :
        cf = ConfigParser.ConfigParser()
        cf.add_section('article')
        cf.set('article', 'startidx', str(arr[0]))
        cf.write(open(self.filename, 'w'))


class Article :
    # ----- attributes -----
    id = ''
    url = ''
    title = ''
    content = ''
    label = -1 # label

    # ----- init method -----
    def __init__(self, data) :
        if len(data) >= 4 :
            self.id = data[0]
            self.url = data[1]
            self.title = data[2]
            self.content = data[3]
            self.label = -1
                
    # ----- import methods -----
    def importSplit(self, data) :
        self.sptitle, self.spcontent = [], []
        if len(data) >= 3 :
            title, content = data[1], data[2]
            for part in title.split(' ') :
                word = Word(part)
                self.sptitle.append(word)
            for part in content.split(' ') :
                word = Word(part)
                self.spcontent.append(word)

    def importLabel(self, data) :
        self.label = int(data[1])

    # ----- print methods -----
    def printArticle(self) :
        line = ''
        line += self.id + u'\t'
        line += self.url + u'\t'
        line += self.title + u'\t'
        line += self.content + u'\t'
        return line.strip()