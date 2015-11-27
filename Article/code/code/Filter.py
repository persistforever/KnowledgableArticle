# -*- encoding = utf-8 -*-
'''
list of filter
1. CollectionFilter
2. ContentLengthFilter
'''

import codecs
import numpy as np
from BasicClass import Article


class CollectionFilter :
    # attributes
    rate = 0.0
    num = 0
    
    # methods
    def __init__(self, num=100) :
        # self.rate = rate
        self.num = num
    
    def filtering(self, artlist) :
        # restnum = int(len(artlist) * self.rate)
        restnum = self.num
        sortedlist = sorted(artlist, key=lambda x: x.collectnum, reverse=True)
        return sortedlist[0:restnum]


class ContentLengthFilter :
    # attributes
    length = 0
    
    # methods
    def __init__(self, length=200) :
        self.length = length
    
    def filtering(self, artlist) :
    	filteredlist = []
    	for article in artlist :
    		if len(article.content) >= self.length :
    			filteredlist.append(article)
        return filteredlist


class TimeWordFilter :
    # attributes
    
    # methods
    def filtering(self, artlist) :
    	filteredlist = []
    	for article in artlist :
            filtered = True
            for word in article.sptitle :
                if word.feature == u't' :
                    filtered = False
            if filtered == True :
            	filteredlist.append(article)
        return filteredlist
