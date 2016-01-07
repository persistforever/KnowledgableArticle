# -*- encoding = gb18030 -*-

# package importing start
import re
import time

# package importing end


class RemoveAdvertice :

    def __init__(self) :
        pass

    def remove_advertice(self, sentences) :
        """ Remove advertice in sentences and return remained index. """
        remained_index = list()
        for idx, sentence in enumerate(sentences) :
            if not self.is_advertice(sentence) :
                remained_index.append(idx)
        return remained_index

    def is_advertice(self, sentence) :
        """ Judge a sentence is a advertice. """
        patterns = [re.compile(p) for p in [u'[\d一二三四五六七八九]折', u'买\d送\d', u'售\d', \
            u'卖\d', u'包邮', u'中奖', u'\d[块元]', u'秒杀']]
        matched = False
        for pattern in patterns :
            if pattern.search(sentence) :
                matched = True
                break
        return matched

        