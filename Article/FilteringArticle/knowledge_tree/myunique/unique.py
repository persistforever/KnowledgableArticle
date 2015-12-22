# -*- encoding = gb18030 -*-

# package importing start
from file.file_operator import TextFileOperator
# package importing end


class Unique :

    def __init__(self) :
        pass

    def unique(self, article_dict) :
        """ Remove duplication of article.
            If two article's participle title has all the same words.
                average the user interactive info.
                combine the id split by '|'.
                combine the url split by '|'.
                reset the pubtime as the earlist pubtime.
        """
        unique_dict = dict()
        unique_article_dict = dict()
        for id in article_dict :
            if 'participle_title' in article_dict[id].keys() :
                key = ''.join(sorted( \
                    [word.to_string() for word in article_dict[id]['participle_title'] \
                    if word.feature != u'w']))
                if key not in unique_dict :
                    unique_dict[key] = []
                unique_dict[key].append(article_dict[id])
        for id in unique_dict :
            key = unique_dict[id][0]['id']
            if key not in unique_article_dict :
                unique_article_dict[key] = unique_dict[id][0]
        return unique_article_dict