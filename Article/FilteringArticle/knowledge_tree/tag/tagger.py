# -*- encoding = gb18030 -*-

# package importing start
import re

from file.file_operator import TextFileOperator
# package importing end

class Tagger :

    def __init__(self) :
        pass

    def read_tag_tree(self, tag_tree_path) :
        """ Read tag tree. """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(tag_tree_path)
        tag_tree = list()
        term = None
        for data in data_list :
            if len(data) >= 1 :
                if data[0] == u'START' :
                    if term != None :
                        tag_tree.append(term)
                    term = list()
                else :
                    type = data[0]
                    term.append((type, data[1:]))
        return tag_tree

    def _constr_dict(self, tag_tree) :
        """ Construct dictionary from tag_tree. """
        entity_dict = dict()
        attr_dict = dict()
        for term in tag_tree :
            value_dict = dict()
            label = term[0][1][0]
            for entity in term[1][1] :
                entity_dict[entity] = label
            for attr, value_list in term[2:] :
                for value in value_list :
                    value_dict[value] = attr
            attr_dict[label] = value_dict
        return entity_dict, attr_dict

    def tag_sentences(self, tag_tree, sentences) :
        """ Tag sentences. """
        entity_dict, attr_dict = self._constr_dict(tag_tree)
        tag_list = list()
        length = len(sentences) - 1
        for idx, sentence in enumerate(sentences) :
            tag = self._tag_sentence_entity(entity_dict, sentence)
            key_sentence = self._find_key_sentence(sentence, tag)
            tag = self._tag_sentence_attributes(attr_dict, key_sentence, tag)
            tag_list.append((sentence, tag))
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return tag_list

    def _tag_sentence_entity(self, entity_dict, sentence) :
        """ Tag entity to each sentence. """
        tag = list()
        for entity in entity_dict :
            if entity in sentence :
                tag.append((u'label', entity_dict[entity]))
                tag.append((u'entity', entity))
        if len(tag) == 2 :
            return tag
        else :
            return list()

    def _tag_sentence_attributes(self, attr_dict, sentence, tag) :
        """ Tag attributes to each sentence. """
        if len(tag) >= 2 :
            for key, value in tag :
                if key == u'label' :
                    label = value
            for value in attr_dict[label] :
                if value in sentence :
                    tag.append((attr_dict[label][value], value))
        return tag

    def _find_key_sentence(self, sentence, tag) :
        """ Find key_sentence of a sentence. """
        stop_list = [u'\uff01', u'\u3010', u'\u3011', u'\uff0c', u'\u3002', \
            u'uff1f', u'\u3001', u'\uff1a', u'\uff08', '\uff09'\
            u'!', u'|', u'~', u',', u'.', u'#', u'-', u'?', u'+']
        sentence = '#' + sentence
        if len(tag) >= 2 :
            for key, value in tag :
                if key == u'entity' :
                    entity = value
            start = -1
            end = sentence.index(entity)
            for idx, letter in enumerate(sentence[0:end+1]) :
                if letter in stop_list :
                    start = idx
            key_sentence = sentence[start+1:idx+len(entity)]
        else :
            key_sentence = sentence[1:]
        return key_sentence