# -*- encoding=gb18030 -*-

import codecs
import random
import sys

def randomSampling(inputpath, outputpath,) :
    with codecs.open(inputpath, 'r', 'gb18030') as fo :
        datalist = [line.strip() for line in fo.readlines()]
    outlist = []
    rate = 1.0 * 1000 / len(datalist)
    for data in datalist :
        if random.random() <= rate :
            outlist.append(data)
    with open(outputpath, 'w') as fw :
        for data in outlist :
            fw.writelines(data.encode('gb18030') + '\n')
        
type = sys.argv[1]
randomSampling('/data1/qspace/data/user/hdpfelicialin/cas/gzhzsk/knowledgable/input/' + type + '/article', \
        '/data1/qspace/data/user/hdpfelicialin/cas/gzhzsk/knowledgable/input/' + type + '/randomsampling')
