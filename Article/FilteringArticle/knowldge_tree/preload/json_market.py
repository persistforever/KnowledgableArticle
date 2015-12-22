# -*- encoding = gb18030 -*-

# package importing start
import re

import json

from file.file_operator import JsonOperator
# package importing end


class JsonMarket :

    def __init__(self) :
        pass

    def sentences_to_json(self, type='create', sentences=[], path='') :
        """ If type is 'create' :
                Initialize the word dictionary using sentences.
            If type is 'load' :
                Initialize the word dictionary from the file.
        """
        if type is 'create' :
            file_operator = JsonOperator()
            json_data = sentences
            file_operator.writing(json_data, path)
        elif type is 'load' :
            file_operator = JsonOperator()
            json_data = file_operator.reading(path)
        print len(json_data)
        return json_data