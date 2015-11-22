# -*- encoding = gb18030 -*-
""" Sub class of Base File Operator """
import codecs
import csv
import os
from base import BaseFileOperator


class CSVFileOperator(BaseFileOperator) :

    def reading(self, file_name):
        """ Read the file as csv file. """
        self.data_list = []
        with codecs.open(file_name, mode='r', encoding='gb18030') as fo :
            csv_reader = csv.reader(fo)
            for line in csv_reader :
                self.data_list.append(line)
        return self.data_list

    def writing(self, data_list, file_name):
        """ Write the file as csv file. """
        with open(self._csv_file(file_name), mode='wb') as fw :
            csv_writer = csv.writer(fw)
            for data in data_list :
                csv_writer.writerow([entry.encode('gb18030') for entry in data])

    def _csv_file(self, file_path) :
        _parent_dir = os.path.pardir
        (file_name, file_type) = os.path.splitext(file_path)
        path = file_name + '.csv'
        return path


class TextFileOperator(BaseFileOperator) :

    def reading(self, file_name):
        """ Read the file as text file. """
        self.data_list = []
        with codecs.open(file_name, mode='rb', encoding='gb18030') as fo :
            for line in fo.readlines() :
                self.data_list.append(line.strip().split('\t'))
        return self.data_list

    def writing(self, data_list, file_name):
        """ Write the file as text file. """
        with open(self._text_file(file_name), mode='wb') as fw :
            for data in data_list :
                line = ''
                for entry in data :
                    line += entry.encode('gb18030') + '\t'
                fw.writelines(line.strip())

    def _text_file(self, file_path) :
        _parent_dir = os.path.pardir
        (file_name, file_type) = os.path.splitext(file_path)
        path = file_name + '.txt'
        return path