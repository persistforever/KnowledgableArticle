# -*- encoding = gb18030 -*-

# package importing start
import re
import time

import file.file_operator as fop
from file.file_operator import JsonOperator, PickleOperator
# package importing end

"""
@ purpose
    If read a big file and convert it to python object such as list or dict.
    Can use Market class to serialize the object.


@ function
    $ load_market
        load market from file.
        input :
            path - path of market file.
        output :
            data - python object such as list or dict.

    $ dump_market
        Dump market to file.
        input :
            market - python object such as list or dict.
            path - path of market file.
"""
class BaseMarket :

    def __init__(self) :
        self._file_operator = fop.BaseFileOperator()

    def load_market(self, path) :
        """ Load market from the file. """
        data = self._file_operator.reading(path)
        print 'The size of the data is %d.' % (len(data))
        return data

    def dump_market(self, market, path) :
        """ Use market to create the word dictionary. """
        start = time.time()
        self._file_operator.writing(market, path)
        end = time.time()
        span = end - start 
        print 'dump market use time %.2f' % span


class PickleMarket(BaseMarket) :

    def __init__(self) :
        BaseMarket.__init__(self)
        self._file_operator = fop.PickleOperator()


class JsonMarket(BaseMarket) :

    def __init__(self) :
        BaseMarket.__init__(self)
        self._file_operator = fop.JsonOperator()