# -*- encoding = gb18030 -*-
""" Sub class of Base File Operator """
import codecs
import csv
import os
import xml.dom.minidom
from base import BaseFileOperator


class CSVFileOperator(BaseFileOperator) :

    def reading(self, file_name):
        """ Read the file as csv file. """
        self.data_list = []
        with open(self._csv_file(file_name), mode='rb') as fo :
            csv_reader = csv.reader(fo)
            for line in csv_reader :
                self.data_list.append([entry.decode('gb18030') for entry in line])
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


class XmlFileOperator(BaseFileOperator) :

    def reading(self, file_name):
        """ Read the file as xml file. """
        dom = xml.dom.minidom.parse(file_name)
        root = dom.documentElement
        nodeset = root.getElementsByTagName('text')
        textset = []
        for node in nodeset :
            urlset.append(node.firstChild.data.strip().split('\t'))
        return urlset

    def writing(self, root, file_name):
        """ Write the file as xml file. """
        impl = xml.dom.minidom.getDOMImplementation()
        dom = impl.createDocument(None, 'xml', None)
        doc = dom.documentElement
        self._sub_writing(root, doc, dom)
        with codecs.open(self._xml_file(file_name), mode='w', encoding='gb18030') as fw :
            dom.writexml(fw, addindent='  ', newl='\n', encoding='gb18030')

    def _sub_writing(self, node, parentdom, dom) :
        nd = dom.createElement('node')
        item = dom.createElement('text')
        itemtext = dom.createTextNode(node.text)
        item.appendChild(itemtext)
        nd.appendChild(item)
        for child in node.child_list :
            self._sub_writing(child, nd, dom)
        parentdom.appendChild(nd)

    def _xml_file(self, file_path) :
        _parent_dir = os.path.pardir
        (file_name, file_type) = os.path.splitext(file_path)
        path = file_name + '.xml'
        return path