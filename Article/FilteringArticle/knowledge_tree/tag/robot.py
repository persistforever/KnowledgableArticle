# -*- encoding = gb18030 -*-

# package importing start
import re
import math
import bitmap

from file.file_operator import TextFileOperator
# package importing end


class Robot :

    def __init__(self) :
        pass

    def tag_sentences(self, tag_tree, sentences) :
        """ Tag sentences. """
        tag_list = list()
        tag_list_show = list()
        untag_sentences = list()
        length = len(sentences) - 1
        for idx, term in enumerate(sentences) :
            aid, sentence = term[0], term[1]
            single, label, entity = self._tag_sentence_entity(tag_tree.entity2label, sentence)
            if single :
                key_sentence = self._find_key_sentence(sentence, label, entity)
                tag, untag_sentence = self._tag_sentence_attributes(tag_tree.value2attr, key_sentence, label, entity)
                tag_list_show.append(tag)
                # store as bit map
                bitlist = [0] * len(tag_tree.index2attr[label])
                strlist = [''] * len(tag_tree.index2attr[label])
                for index in tag_tree.index2attr[label] :
                    attr = tag_tree.index2attr[label][index]
                    strlist[index] = ['0'] * len(tag_tree.value2index[label][attr])
                for attr, value in tag :
                    strlist[tag_tree.attr2index[label][attr]][ \
                        tag_tree.value2index[label][attr][value]] = '1'
                for idx, string in enumerate(strlist) :
                    bitlist[idx] = bitmap.BitMap.fromstring(''.join(string[::-1])).bitmap[0]
                tag_list.append((aid, label, entity, bitlist))
                if untag_sentence != '' :
                    untag_sentences.append([untag_sentence, sentence])
            else :
                tag_list_show.append(list())

            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return tag_list, tag_list_show, untag_sentences

    def question_and_answer(self, string, sentences, tags, tag_tree) :
        """ Robot find tags accordding to querys and ask the tags.
            User complete tags and answer to robot.
        """
        querys = [self._tag_sentence_entity(tag_tree.entity2label, string), list()]
        if len(querys) >= 2 :
            while True :
                last_sentences_len = len(sentences)
                querys[0], untag_sentence = self._tag_sentence_attributes(tag_tree.value2attr, string, querys[0])
                sentences, tags = self._find_condidate_article(querys, sentences, tags)
                if len(sentences) > 5 and len(sentences) != last_sentences_len :
                    ask_tags = self._select_tags(querys[0][0][1], tags, tag_tree)
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

    '''
    def _tag_sentence_entity(self, entity2label, sentence) :
        """ Tag entity to each sentence. """
        tag = list()
        for entity in entity2label :
            if entity in sentence :
                tag.append((u'label', entity2label[entity]))
                tag.append((u'entity', entity))
        if len(tag) == 2 :
            return tag
        else :
            return list()

    def _tag_sentence_attributes_old(self, value2attr, sentence, tag) :
        """ Tag attributes to each sentence. """
        if len(tag) >= 2 :
            for key, value in tag :
                if key == u'label' :
                    label = value
            for value in value2attr[label] :
                if value in sentence :
                    tag.append((value2attr[label][value], value))
        return tag
    '''

    def _tag_sentence_entity(self, entity2label, sentence) :
        """ Tag entity to each sentence. """
        sentence = '#' + sentence
        label = list()
        entity = list()
        start = end = len(sentence)-1
        inited = True
        while end >= 0 and start >= 0 :
            condidate = sentence[start:end+1]
            if inited :
                inited = False
                tec = list() # target_endswith_condidate
                cet = list() # condidate_endswith_target
                for value in entity2label :
                    if value.endswith(condidate) :
                        cet.append(value)
            new_cet = list()
            for idx, value in enumerate(cet) :
                if value.endswith(condidate) :
                    new_cet.append(value)
            cet = new_cet
            for idx, value in enumerate(cet) :
                if condidate.endswith(value) :
                    tec.append(value)
            if len(cet) > 0 :
                start -= 1
            else :
                inited = True
                if len(tec) > 0 :
                    ett = max(tec, key=lambda x: len(x))
                    label.append(entity2label[ett])
                    entity.append(ett)
                    end = start
                else :
                    start -= 1
                    end = start
        single = False
        if len(entity) == 1 :
            single = True
            return single, label[0], entity[0]
        else :
            return single, list(), list()

    def _tag_sentence_attributes(self, value2attr, sentence, label, entity) :
        """ Tag attributes to each sentence. """
        old_sentence = sentence
        sentence = '#' + sentence
        untag_sentence = ''
        tag = list()
        value_dict = value2attr[label]
        value_dict[entity] = u'entity'
        start = end = len(sentence)-1
        inited = True
        while end >= 0 and start >= 0 :
            condidate = sentence[start:end+1]
            if inited :
                inited = False
                tec = list() # target_endswith_condidate
                cet = list() # condidate_endswith_target
                for value in value_dict :
                    if value.endswith(condidate) :
                        cet.append(value)
            new_cet = list()
            for idx, value in enumerate(cet) :
                if value.endswith(condidate) :
                    new_cet.append(value)
            cet = new_cet
            for idx, value in enumerate(cet) :
                if condidate.endswith(value) :
                    tec.append(value)
            if len(cet) > 0 :
                start -= 1
            else :
                inited = True
                if len(tec) > 0 :
                    value = max(tec, key=lambda x: len(x))
                    tag.append((value2attr[label][value], value))
                    end = start
                else :
                    start -= 1
                    end = start
                    untag_sentence += condidate[::-1]
        untag_sentence = untag_sentence[::-1][1:]
        outtag = [(key, value) for key, value in tag if key != u'entity']
        return outtag, untag_sentence

    def _find_key_sentence(self, sentence, label, entity) :
        """ Find key_sentence of a sentence. """
        stop_list = [u'\uff01', u'\u3010', u'\u3011', u'\uff0c', u'\u3002', \
            u'uff1f', u'\u3001', u'\uff1a', u'\uff08', '\uff09'\
            u'!', u'|', u'~', u',', u'.', u'#', u'-', u'?', u'+']
        sentence = '#' + sentence
        start = -1
        end = sentence.index(entity)
        for idx, letter in enumerate(sentence[0:end+1]) :
            if letter in stop_list :
                start = idx
        key_sentence = sentence[start+1:idx+len(entity)]
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

    def _select_tags(self, label, tags, tag_tree, n_tops=3) :
        """ select a tag with n_tops values. """
        ask_tags = ['', list()]
        max_sum_entropy = 0.0
        for attr in set(tag_tree.value2attr[label].values()) :
            attr_entropy = 0.0
            value_set = [value for value in tag_tree.value2attr[label] if tag_tree.value2attr[label][value] == attr]
            x_array = [0] * len(tags)
            p_array = [0.0] * len(value_set)
            for idx, tag in enumerate(tags) :
                x_array[idx] = -1
                for a, v in tag :
                    if a==attr and v in value_set :
                        x_array[idx] = value_set.index(v)
            for value_idx in range(0, len(value_set)) :
                p_array[value_idx] = 1.0 * len([x for x in x_array if x == value_idx]) / len(x_array)
            sum_entropy = 0.0
            sorted_array = sorted(enumerate(p_array), key=lambda x: x[1], reverse=True)[0:n_tops]
            for value_idx, score in sorted_array :
                h = -1.0 * score * math.log(score) if score != 0.0 else 0.0
                sum_entropy += h
            t = 1 - sum([x[1] for x in sorted_array])
            sum_entropy += -1.0 * t * math.log(t) if t != 0.0 else 0.0
            if sum_entropy >= max_sum_entropy :
                max_sum_entropy = sum_entropy
                ask_tags[0] = attr
                ask_tags[1] = [value_set[idx] for idx, value in sorted_array if value > 0]
        return ask_tags