# -*- encoding = gb18030 -*-

# package importing start
import re
import math

from file.file_operator import TextFileOperator
# package importing end

class Robot :

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
        self.entity_dict, self.attr_dict = self._constr_dict(tag_tree)
        return tag_tree

    def tag_sentences(self, tag_tree, sentences) :
        """ Tag sentences. """
        tag_list = list()
        length = len(sentences) - 1
        for idx, sentence in enumerate(sentences) :
            tag = self._tag_sentence_entity(self.entity_dict, sentence)
            key_sentence = self._find_key_sentence(sentence, tag)
            tag = self._tag_sentence_attributes(self.attr_dict, key_sentence, tag)
            tag_list.append(tag)
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return tag_list

    def question_and_answer(self, string, sentences, tags) :
        """ Robot find tags accordding to querys and ask the tags.
            User complete tags and answer to robot.
        """
        querys = [self._tag_sentence_entity(self.entity_dict, string), list()]
        if len(querys) >= 2 :
            while True :
                last_sentences_len = len(sentences)
                querys[0] = self._tag_sentence_attributes(self.attr_dict, string, querys[0])
                sentences, tags = self._find_condidate_article(querys, sentences, tags)
                if len(sentences) > 5 and len(sentences) != last_sentences_len :
                    ask_tags = self._select_tags(querys[0][0][1], tags)
                    print u'现在有', len(sentences), u'篇候选文章'
                    print u'你想要那种', ask_tags[0], u'?', 
                    for value in ask_tags[1] :
                        print value,
                    print 
                    idx = int(raw_input())
                    if idx >= 0 :
                        querys[0].append((ask_tags[0], ask_tags[1][idx]))
                    else :
                        for value in ask_tags[1] :
                            querys[1].append((ask_tags[0], value))
                else :
                    for sentence in sentences :
                        print sentence
                    return sentences

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

    def _tag_sentence_attributes1(self, attr_dict, sentence, tag) :
        """ Tag attributes to each sentence. """
        if len(tag) >= 2 :
            for key, value in tag :
                if key == u'label' :
                    label = value
            for value in attr_dict[label] :
                if value in sentence :
                    tag.append((attr_dict[label][value], value))
        return tag

    def _tag_sentence_attributes(self, attr_dict, sentence, tag) :
        """ Tag attributes to each sentence. """
        if len(tag) >= 2 :
            for key, value in tag :
                if key == u'label' :
                    label = value
            value_dict = attr_dict[label]
            start = end = len(sentence)-1
            while end >= 0 and start >= 0 :
                condidate_tag = list()
                condidate_word = sentence[start:end+1]
                for value in value_dict :
                    if value.endswith(condidate_word) :
                        condidate_tag.append(value)
                if len(condidate_tag) > 1 :
                    start -= 1
                elif len(condidate_tag) == 1 and condidate_tag[0] == condidate_word :
                    tag.append((attr_dict[label][condidate_tag[0]], condidate_tag[0]))
                    end = start - 1
                    start = start - 1
                else :
                    end = start - 1
                    start = start - 1
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

    def _find_condidate_article(self, querys, sentences, tags) :
        """ Find condidate article according to querys. """
        condidate_sentences = list()
        condidate_tags = list()
        for idx, tag in enumerate(tags) :
            condidated = True
            values = [value for attr, value in tag[1:]]
            for query in querys[0][1:] :
                if query[1] not in values :
                    condidated = False
            for query in querys[1][0:] :
                if query[1] in values :
                    condidated = False
            if condidated :
                condidate_sentences.append(sentences[idx])
                condidate_tags.append(tags[idx])
        return condidate_sentences, condidate_tags

    def _select_tags(self, label, tags, n_tops=3) :
        """ select a tag with n_tops values. """
        ask_tags = ['', list()]
        max_sum_entropy = 0.0
        for attr in set(self.attr_dict[label].values()) :
            attr_entropy = 0.0
            value_set = [value for value in self.attr_dict[label] if self.attr_dict[label][value] == attr]
            x_array = [0] * len(tags)
            h_array = [0.0] * len(value_set)
            for idx, tag in enumerate(tags) :
                x_array[idx] = -1
                for a, v in tag :
                    if a==attr and v in value_set :
                        x_array[idx] = value_set.index(v)
            for value_idx in range(0, len(value_set)) :
                p = 1.0 * len([x for x in x_array if x == value_idx]) / len(x_array)
                if p == 0 :
                    h_array[value_idx] = 0.0
                else :
                    h_array[value_idx] = -1.0 * p * math.log(p)
            sum_entropy = 0.0
            sorted_array = sorted(enumerate(h_array), key=lambda x: x[1], reverse=True)[0:n_tops]
            for value_idx, score in sorted_array :
                sum_entropy += score
            if sum_entropy >= max_sum_entropy :
                max_sum_entropy = sum_entropy
                ask_tags[0] = attr
                ask_tags[1] = [value_set[idx] for idx, value in sorted_array if value > 0]
        return ask_tags