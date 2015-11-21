# -*- encoding = gb18030 -*-
""" Test of basic """

import sys
import unittest
from corpus import Corpus


class TestCorpus(unittest.TestCase) :

    def test_path(self) :
        corpus = Corpus()
        print 
        raw_input()


if __name__ == '__main__' :
    unittest.main()