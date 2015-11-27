# -*- encoding = gb18030 -*-

# package importing start
from file.file_operator import TextFileOperator
from basic.word import Word
# package importing end


class SynonymySearcherBase :

    def __init__(self) :
        self.query_list = []
        self.synonymy_list = []

    def read_querys(self, querys_path) :
        """ Read query words. 
            Each line of the file is a query word.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(querys_path)
        for data in data_list :
            if len(data) >= 1 :
                self.query_list.append(Word(data[0]))

    def find_synonymy_words(self) :
        """ find synonymy words of the query_list. 
            This is a abstract function and MUST override. 
            Return the synonymy word list. 
        """

    def write_synonymys(self, synonymys_path) :
        """ Write synonymy words.
            Each line of the file is a synonymy word.
        """
        file_operator = TextFileOperator()
        data_list = []
        for synonymy in self.synonymy_list :
            data = []
            data.append(synonymy.to_string())
            data.append(synonymy.score)
            data_list.append(data)
        file_operator.writing(data_list, synonymys_path)