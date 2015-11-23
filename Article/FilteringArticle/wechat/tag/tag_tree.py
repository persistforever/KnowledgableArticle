# -*- encoding = gb18030 -*-
""" Class tree of the tag. """

import numpy as np
import lda

class TreeNode :

    def __init__(self, level, child_num) :
        self.level = level
        self.child_num = child_num
        self.word_list = []
        self.article_list = []
        self.word_topic_dict = dict()
        self.doc_topic_dict = dict()
        self.child_list = []

    def set_params(self, **params) :
        """ Set parameters of the tree node. """

        for key, value in params.iteritems() :
            setattr(self, key, value)

    def split_node(self, index_article, index_word) :
        """ Split tree node into #child_num child nodes. """

        article_bagofword = []
        for article_idx in self.article_list :
            article_bagofword.append(index_article[article_idx].bagofword_vector)
        article_bagofword = np.array(article_bagofword)
        model = lda.LDA(n_topics=self.child_num, n_iter=200, random_state=1).fit(article_bagofword)
        self.doc_topic_dict = dict()
        for row in range(model.doc_topic_.shape[0]) :
            topic_disb = model.doc_topic_[row, :].tolist()
            s = sum(topic_disb)
            for col in range(len(topic_disb)) :
                topic_disb[col] = 1.0 * topic_disb[col] / s
            self.doc_topic_dict[self.article_list[row]] = topic_disb

        self.word_topic_dict = dict()
        for row in range(model.topic_word_.shape[1]) :
            topic_disb = model.topic_word_[:, row].tolist()
            s = sum(topic_disb)
            for col in range(len(topic_disb)) :
                topic_disb[col] = 1.0 * topic_disb[col] / s
            self.word_topic_dict[index_word[row]] = topic_disb

        for idx in range(self.child_num) :
            node = TreeNode(self.level+1, self.child_num-1)
            self.child_list.append(node)

        for article_idx in self.doc_topic_dict :
            dp_list = [t for t in enumerate(self.doc_topic_dict[article_idx])]
            node_idx = max(dp_list, key=lambda x: x[1])[0]
            dp_value = self.doc_topic_dict[article_idx][node_idx]
            if dp_value >= 0.9 :
                self.child_list[node_idx].article_list.append(article_idx)
        for word in self.word_topic_dict :
            dp_list = [t for t in enumerate(self.word_topic_dict[word])]
            node_idx = max(dp_list, key=lambda x: x[1])[0]
            dp_value = self.word_topic_dict[word][node_idx]
            if dp_value >= 0.9 :
                self.child_list[node_idx].word_list.append([word, dp_value])

    def print_node(self) :
        """ Print the key infomation of the node. """

        outstr = ''
        num = 0
        self.word_list = sorted(self.word_list, key=lambda x: x[1], reverse=True)
        for word, dp_value in self.word_list :
            if num >= 10 :
                break
            if word.feature == u'n' :
                num += 1
                outstr += word.name + '\t'
        return outstr.strip()