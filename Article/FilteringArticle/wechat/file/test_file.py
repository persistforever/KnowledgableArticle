# -*- encoding = gb18030 -*-
""" Test of path manager """

import sys
import unittest
from path_manager import PathManager
from file_operator import TextFileOperator


class TestPathManager(unittest.TestCase) :

    def test_path(self) :
        pm = PathManager()
        print pm.csv_file(pm.get_input_article())
        raw_input()


class TestFileManager(unittest.TestCase) :

    def test_csv(self) :
        pm = PathManager()
        _file_name = pm.get_output_article()
        text = TextFileOperator()
        print len(text.reading(_file_name)[0])
        raw_input()


if __name__ == '__main__' :
    unittest.main()