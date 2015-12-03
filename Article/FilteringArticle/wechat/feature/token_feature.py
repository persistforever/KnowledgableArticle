# -*- encoding = gb18030 -*-

# package importing start
# package importing end


class TokenExtractor :
    
    def __init__(self, sp_path, pc_path) :
        self.spdict = self.importSpDict(self.sppath)
        self.pcdict = self.importPcDict(self.pcpath)
        
    def importSpDict(self, sppath) :
        spdict = dict()
        with codecs.open(sppath, 'r', 'gb18030') as fo :
            for line in fo.readlines() :
                if line.strip() not in spdict :
                    spdict[line.strip()] = None
        return spdict
        
    def importPcDict(self, pcpath) :
        pcdict = dict()
        with codecs.open(pcpath, 'r', 'gb18030') as fo :
            for line in fo.readlines() :
                if line.strip() not in pcdict :
                    pcdict[line.strip()] = None
        return pcdict
    
    def extractFeature(self, artlist) :
        for article in artlist :
            article.contentlength = len(article.content)
            article.titlelength = len(article.title)
            article.wordnumtl = len(article.sptitle) 
            article.wordnumct = len(article.spcontent)
            tlworddict = dict()
            for word in article.sptitle :
                if word.name not in tlworddict :
                    tlworddict[word.name] = None
            ctworddict = dict()
            for word in article.spcontent :
                if word.name not in ctworddict :
                    ctworddict[word.name] = None
            article.distwordnumct = len(ctworddict)
            article.distwordnumtl = len(tlworddict)
            article.puncnumct = sum([1 for char in article.content if char in self.pcdict])
            article.puncnumtl = sum([1 for char in article.title if char in self.pcdict])
            pgspchar = u'\u3000'
            stspchar = '['
            for sp in self.spdict :
                stspchar += sp
            stspchar += ']'
            paragraphlist = re.split(pgspchar, article.content)
            article.paragraphnum = len(paragraphlist)
            article.sentencenum = 0
            article.avgpgstnum = 0.0
            article.avgstlength = 0.0
            for paragraph in paragraphlist :
                sentencelist = re.split(stspchar, paragraph)
                article.sentencenum += len(sentencelist)
                article.avgpgstnum += len(sentencelist)
                for sentence in sentencelist :
                    article.avgstlength += len(sentence)
            article.avgstlength /= 1.0 * article.sentencenum
            article.avgpgstnum /= 1.0 * article.paragraphnum
