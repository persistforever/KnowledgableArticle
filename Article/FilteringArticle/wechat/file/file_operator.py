# -*- encoding = gb18030 -*-
""" Sub class of Base File Operator """
import codecs
import csv
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
        with open(file_name, mode='wb') as fw :
            csv_writer = csv.writer(fw)
            for data in data_list :
                csv_writer.writerow(data)


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
        with open(file_name, mode='wb') as fw :
            for data in data_list :
                line = ''
                for data in data_list :
                    line += str(data) + '\t'
                fw.writelines(line.strip())