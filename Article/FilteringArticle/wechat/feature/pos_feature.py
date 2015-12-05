# -*- encoding = gb18030 -*-

# package importing start
import numpy as np

from file.file_operator import TextFileOperator
from feature.base import BaseExtractor
# package importing end


class PosExtractor(BaseExtractor) :

    def __init__(self, w=10, pos_path='') :
        BaseExtractor.__init__(self)

        self.w = w
        self.noun = [5, 11, 12, 14, 15, 16, 37]
        self.adjective = [3, 22, 23, 28]
        self.verb = [2, 4, 29, 45]
        self.adverb = [9, 27]
        self.conjunction = [24, 39]
        self.mood = [36, 46, 10]
        self.quantity = [34, 38, 27, 18]
        self.pos_dict = self._read_dictionary(pos_path)
        
    def _read_dictionary(self, pos_path) :
        file_operator = TextFileOperator()
        data_list = file_operator.reading(pos_path)
        dictionary = dict()
        for data in data_list :
            if len(data) >= 1 :
                if data[0] not in dictionary :
                    dictionary[data[0]] = 0
        return dictionary
    
    def extractFeature(self, article_list) :
        for article in article_list :
            num_list = []
            for x in range(0, min(len(article.split_content), 500) - self.w + 1) :
                pos_hist = dict()
                for key in self.pos_dict.keys() :
                    pos_hist[key] = 0
                for i in range(x, x + self.w) :
                    if article.split_content[i].feature in pos_hist :
                        pos_hist[article.split_content[i].feature] += 1
                num_list.append(pos_hist.values())
            mean_set, var_set = [], []
            for j in range(len(num_list[0])) :
                mean_set.append(np.mean([line[j] for line in num_list]))
                var_set.append(np.var([line[j] for line in num_list]))
            navg, nvar = 0.0, 0.0
            aavg, avar = 0.0, 0.0
            vavg, vvar = 0.0, 0.0
            davg, dvar = 0.0, 0.0
            cavg, cvar = 0.0, 0.0
            mavg, mvar = 0.0, 0.0
            qavg, qvar = 0.0, 0.0
            for idx in self.noun :
                navg += mean_set[idx]
                nvar += var_set[idx]
            for idx in self.adjective :
                aavg += mean_set[idx]
                avar += var_set[idx]
            for idx in self.verb :
                vavg += mean_set[idx]
                vvar += var_set[idx]
            for idx in self.adverb :
                davg += mean_set[idx]
                dvar += var_set[idx]
            for idx in self.conjunction :
                cavg += mean_set[idx]
                cvar += var_set[idx]
            for idx in self.mood :
                mavg += mean_set[idx]
                mvar += var_set[idx]
            for idx in self.quantity :
                qavg += mean_set[idx]
                qvar += var_set[idx]
            article.set_features(navg=navg, nvar=nvar, aavg=aavg, avar=avar, vavg=vavg, \
                vvar=vvar, davg=davg, dvar=dvar, cavg=cavg, cvar=cvar, mavg=mavg, \
                mvar=mvar, qavg=qavg, qvar=qvar)