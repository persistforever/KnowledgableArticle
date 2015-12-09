# -*- encoding = gb18030 -*-
""" question and anster system clustering article. """

# package importing start
import codecs
import numpy as np

import gensim

from basic.article import Article
from basic.word import Word
from file.path_manager import PathManager
from file.file_operator import TextFileOperator
from qa.word_cluster import WordCluster
from sklearn.cluster import KMeans, SpectralClustering
from sklearn import metrics
# package importing end


class ArticleCluster :

    def __init__(self, corpus_path='', tfidf_path='', dict_path='', w2v_path='') :
        self.corpus_path = corpus_path
        self.tfidf_path = tfidf_path
        self.dict_path = dict_path
        self.w2v_path = w2v_path
        self.mmcorpus, self.tfidf_model, self.dictionary, self.word2vec = self._read_model()

    def _read_model(self) :
        """ Read tfidf models. """
        mmcorpus = gensim.corpora.MmCorpus(self.corpus_path)
        tfidf_model = gensim.models.TfidfModel.load(self.tfidf_path)
        dictionary = gensim.corpora.Dictionary.load(self.dict_path)
        word2vec = gensim.models.Word2Vec.load(self.w2v_path)
        return mmcorpus, tfidf_model, dictionary, word2vec

    def article_clustering(self, article_list, query_list) :
        """ clustering article's keyword accordding to query. """
        while len(article_list) > 1 :
            print len(article_list)
            word_dict = self._article_tfidf(article_list, query_list)
            for article in article_list :
                print article.id.encode('gb18030'), 
                for w in article.tag_list :
                    print w.name.encode('gb18030'), 
                print
            print len([article for article in article_list if article.tag_list==[]])
            if len([article for article in article_list if article.tag_list!=[]]) <= 1 :
                break
            cls = WordCluster(word_dict, n_cluster=3)
            self.label_list = cls.get_label_list()
            outstr = 'which do you want? '
            for key, word_list in self.label_list :
                outstr += key + ' '
            outstr.strip().encode('gb18030')
            seq = int(raw_input(outstr))
            query_list.append(self.label_list[seq][0])
            perticular_article_list = []
            for article in article_list :
                for word in self.label_list[seq][1] :
                    if word in [w.name for w in article.tag_list] :
                        perticular_article_list.append(article)
                    break
            article_list = perticular_article_list
        if len(article_list) > 0 :
            print [article.id for article in article_list][0]

    def _article_tagging(self, lucene_list, query_list) :
        """ tagging each article. """
        word_dict = dict()
        for article in article_list :
            article.set_params(tag_list=[])
            keyword_dict = dict()
            for keyword, tfidf in article.keyword_list[0:100] :
                for query in query_list :
                    distance = self._keyword_query_distance(keyword, query, article.sub_sentence)
                    if keyword not in keyword_dict :
                        keyword_dict[keyword.name] = []
                    if distance != 0 :
                        keyword_dict[keyword.name].append(1.0 * distance * tfidf)
            for keyword in keyword_dict :
                if keyword_dict[keyword] != [] :
                    keyword_dict[keyword] = 1.0 * sum(keyword_dict[keyword]) / len(keyword_dict[keyword])
                else :
                    keyword_dict[keyword] = 0
            for word, score, in sorted(keyword_dict.iteritems(), key=lambda x: x[1], reverse=True)[0:100] :
                if score >= 3 : 
                    word_object = Word(word)
                    article.tag_list.append(word_object)
                    if word_object.name not in word_dict :
                        if word_object.name not in query_list :
                            word_dict[word_object.name] = 0
                    if word_object.name not in query_list :
                        word_dict[word_object.name] += 1
        return word_dict

    def user_choosing(self) :
        word_dict, tag_list = self._article_keyword()
        word_dict = self._word_clustering(word_dict)

    def _article_tfidf(self, lucene_list, query_list) :
        """ tagging each article. """
        word_dict = dict()
        tag_list = []
        for idx, text in enumerate([self.mmcorpus[index] for index in lucene_list]) :
            tag = []
            for query in query_list :
                for keyword, tfidf in filter(lambda x: x[1] > 0.6, self.tfidf_model[text]) :
                    if self.dictionary[keyword] in self.word2vec.vocab and \
                        query in self.word2vec.vocab :
                        if self.dictionary[keyword] not in word_dict :
                            word_dict[self.dictionary[keyword]] = []
                        word_dict[self.dictionary[keyword]].append( \
                            tfidf * self.word2vec.similarity(self.dictionary[keyword], query))
                        tag.append(keyword)
            tag_list.append(tag)
        word_dict = {word:None for word, lst in word_dict.iteritems() if sum(lst)>0}
        return word_dict, tag_list

    def _article_keyword(self) :
        """ tagging each article. """
        word_dict = dict()
        tag_list = []
        for idx, text in enumerate(self.mmcorpus) :
            tag = []
            for keyword, tfidf in filter(lambda x: x[1] > 0.2, self.tfidf_model[text]) :
                if self.dictionary[keyword] in self.word2vec.vocab :
                    if self.dictionary[keyword] not in word_dict :
                        word_dict[self.dictionary[keyword]] = []
                    word_dict[self.dictionary[keyword]].append(tfidf)
                    tag.append(self.dictionary[keyword])
            tag_list.append(tag)
        word_dict = {word:None for word, lst in word_dict.iteritems() if sum(lst)>0}
        return word_dict, tag_list

    def _word_clustering(self, word_dict) :
        """ clustering the word. """
        word_set = []
        for word in word_dict.keys() :
            word_set.append(self.word2vec[word])
        word_set = np.array(word_set)
        max_labels_, max_evaluation = np.zeros([len(word_dict), 1]), 0.08
        for n in range(2, 10) :
            cls = SpectralClustering(n_clusters=n, assign_labels='discretize').fit(word_set)
            score = metrics.silhouette_score(word_set, cls.labels_, metric='cosine')
            if score > max_evaluation :
                max_evaluation = score
                max_labels_ = cls.labels_
        for idx in range(max_labels_.shape[0]) :
            word_dict[word_dict.keys()[idx]] = max_labels_[idx]
        for word in word_dict :
            print word, word_dict[word]
        return word_dict

    def ploting(self, word_set, labels) :
        """ Plot word_dict. """
        from sklearn.manifold import TSNE
        import matplotlib.pyplot as plt
        tsne = TSNE(n_components=2, random_state=0)
        color = ['r', 'g', 'b', 'y', 'm']
        for point, label in zip(tsne.fit_transform(word_set), labels)  :
            plt.scatter(point[0], point[1], color=color[label])
        plt.show()

    def _cluster_likelihood(self, word_set, labels_) :
        """ Calculate the likelihood of cluster. """

    def _keyword_query_distance(self, keyword, query, sub_sentence) :
        """ calculate distance between keyword and query. """
        distance = 0.0
        for sentence in sub_sentence :
            sentence_word = [word.name for word in sentence]
            if keyword.name in sentence_word and query in sentence_word :
                # print ''.join([word.name for word in sentence])
                distance += abs(sentence_word.index(keyword.name) - \
                    sentence_word.index(query))
        if distance != 0 :
            distance = 1.0 / distance
        return distance