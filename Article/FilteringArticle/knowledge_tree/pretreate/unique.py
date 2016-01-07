# -*- encoding = gb18030 -*-

# package importing start
from file.file_operator import TextFileOperator
# package importing end


class Unique :

    def __init__(self) :
        pass

    def unique(self, participle_list) :
        """ Remove duplication of article.
            If two article's participle title has all the same words.
                average the user interactive info.
                combine the id split by '|'.
                combine the url split by '|'.
                reset the pubtime as the earlist pubtime.
        """
        unique_dict = dict()
        unique_list = list()
        for idx, participle in enumerate(participle_list) :
            key = ''.join(sorted( [word.name for word in participle if word.feature != u'w']))
            if key not in unique_dict :
                unique_dict[key] = list()
            unique_dict[key].append(idx)
        for id in unique_dict :
            unique_list.append(unique_dict[id][0])
        return sorted(unique_list)