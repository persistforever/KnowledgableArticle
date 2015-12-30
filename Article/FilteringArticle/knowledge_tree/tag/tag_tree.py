﻿# -*- encoding = gb18030 -*-

# package importing start
import re
import math

from file.file_operator import TextFileOperator
# package importing end


class TagTreeNode :

    def __init__(self) :
        pass


class TagTree :

    def __init__(self, cmd_list) :
        self.root = TagTreeNode()
        self.root.labels = dict()
        self.root.global_attrs = dict()
        self._constr_tag_tree(cmd_list)
        self._constr_dict()

    def _constr_tag_tree(self, cmd_list) :
        """ Construct tag tree from tag list. """
        for cmd in cmd_list :
            [word.upper() for word in cmd]
            func = cmd[0]
            params = cmd[1:] 

            if func == u'LABEL' :
                for label in params :
                    self.add_label(label)
            elif func == u'ENTITY' :
                for entity in params[1:] :
                    self.add_entity(params[0], entity)
            elif func == u'LCATTR' :
                for attr in params[1:] :
                    self.add_local_attr(params[0], attr)
            elif func == u'LCVALUE' :
                for value in params[2:] :
                    self.add_local_value(params[0], params[1], value)
            elif func == u'GLATTR' :
                for attr in params :
                    self.add_global_attr(attr)
            elif func == u'GLVALUE' :
                for value in params[1:] :
                    self.add_global_value(params[0], value)

    def _constr_dict(self) :
        """ Construct dict. """
        self.entity2label = dict()
        for label in self.root.labels :
            for entity in self.root.labels[label].entitys :
                self.entity2label[entity] = label
        self.value2attr = dict()
        for label in self.root.labels :
            self.value2attr[label] = dict()
            for attr in self.root.labels[label].local_attrs :
                for value in self.root.labels[label].local_attrs[attr] :
                    self.value2attr[label][value] = attr
            for attr in self.root.global_attrs :
                for value in self.root.global_attrs[attr] :
                    self.value2attr[label][value] = attr

    def add_label(self, label) :
        """ Add label to root node. """
        label_node = TagTreeNode()
        label_node.entitys = list()
        label_node.local_attrs = dict()
        self.root.labels[label] = label_node

    def add_entity(self, label, entity) :
        """ Add entity to label node. """
        self.root.labels[label].entitys.append(entity)

    def add_local_attr(self, label, attr) :
        """ Add local attribute to label node. """
        self.root.labels[label].local_attrs[attr] = list()

    def add_local_value(self, label, attr, value) :
        """ Add value to local attribute node. """ 
        self.root.labels[label].local_attrs[attr].append(value)

    def add_global_attr(self, attr) :
        """ Add global attribute to root node. """
        self.root.global_attrs[attr] = list()

    def add_global_value(self, attr, value) :
        """ Add value to global attribute node. """
        self.root.global_attrs[attr].append(value)