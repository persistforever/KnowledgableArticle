# -*- encoding = gb18030 -*-

# package importing start
import numpy as np

from article import Article
from article import Word
from file.file_operator import BaseFileOperator, CSVFileOperator, TextFileOperator
# package importing end



class Corpus(object) :

    def __init__(self) :
        self.article_list = []

    def read_article_list(self, article_path) :
        """ Read article list.
            Each row of the file is a article.
            column[0] of the file is the id of article.
            column[1] of the file is the url of article.
            column[2] of the file is the title of article.
            column[3] of the file is the content of article.
            * This function MUST be the first to read article.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(article_path)
        entry_list = data_list[0]
        for data in data_list[1:] :
            if len(data) >= len(entry_list) :
                article = Article()
                for idx in range(len(data)) :
                    cmd = entry_list[idx] + '<=>' + data[idx]
                    article.set_attributes(cmd)
                self.article_list.append(article)
        self._constr_dict_id()
        self._constr_dict_index()

    def read_participle_title_list(self, split_path) :
        """ Read participle title list.
            Each row of the file is a article.
            column[0] of the file is the id of article.
            column[1] of the file is the participle_title of article.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(split_path)
        for data in data_list[1:] :
            if len(data) >= 2 :
                id = data[0]
                if id in self._id_article :
                    article = self._id_article[id]
                    article.participle_title = [Word(part, sp_char=':') for part in data[1].split(' ')]

    def read_participle_content_list(self, split_path) :
        """ Read participle content list.
            Each row of the file is a article.
            column[0] of the file is the id of article.
            column[1] of the file is the participle_title of article.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(split_path)
        for data in data_list[1:] :
            if len(data) >= 2 :
                id = data[0]
                if id in self._id_article :
                    article = self._id_article[id]
                    article.participle_content = [Word(part, sp_char=':') for part in data[1].split(' ')]

    def sub_title_info(self, sentence_path) :
        """ Read sentence list.
            Each row of the file is a sentence.
            column[0] of the file is the id of article.
            column[1] of the file is the sub_sentence of article.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(sentence_path)
        for data in data_list :
            if len(data) >= 2 :
                id = data[0]
                if id in self._id_article :
                    article = self._id_article[id]
                    article.import_sub_sentence(data)

    def read_content_sentence_list(self, sentence_path) :
        """ Read content sentence list.
            Each row of the file is a sentence.
            column[0] of the file is the id of article.
            column[1] of the file is the splited sentence of article.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(sentence_path)
        for data in data_list[1:] :
            if len(data) >= len(entry_list) :
                article = Article()
                id = data[0]
                if id in self._id_article :
                    article = self._id_article[id]
                    article.import_sub_sentence(data)
                    
    def read_wordbag(self, wordbag_path, sp_char=':') :
        """ Read word bag.
            Each row of the file is a word.
            column[0] of the file is the word and feature.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(wordbag_path)
        wordbag = []
        for data in data_list :
            if len(data[0].split(sp_char)) >= 2 :
                word = Word(data[0], sp_char=sp_char)
                wordbag.append(word)
        return wordbag

    def read_lucene_list(self, lucene_path) :
        """ Read lucene list.
            Each row of the file is a article.
            column[0] of the file is the id of article.
            column[1] of the file is the url of article.
            column[2] of the file is the title of article.
            column[3] of the file is the content of article.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(lucene_path)
        lucene_list = []
        for data in data_list :
            if len(data) >= 4 :
                id = data[0]
                if id in self._id_index :
                    lucene_list.append(self._id_index[id])
        return lucene_list

    def read_train_dataset(self, train_path='') :
        """ Read train_dataset from input/traindata.
        Each row of the file is a article.
        Each column[0:3] of the file is the attributes of the article. 
        Each column[3:-1] of the file is the feature of the article. 
        column[-1] of the file is the label of the article. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(train_path)
        dataset_list = [np.array(data[0:-1]) for data in data_list[1:]]
        label_list = [line[-1] for line in data_list[1:]]
        self.train_dataset = self._normalization(np.array(dataset_list, dtype=float))
        self.train_label = np.array(label_list, dtype=float)
        print 'reading train dataset finished ...'

    def read_test_dataset(self, test_path='') :
        """ Read test_dataset from input/traindata.
        Each row of the file is a article.
        column[0] of the file is the id of the article.
        Each column[1:] of the file is the feature of the article. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(test_path)
        test_dataset = np.array([np.array(line[3:]) for line in data_list[1:]], dtype=float)
        self.test_dataset = self._normalization(test_dataset)
        entry_list = data_list[0]
        for data in data_list[1:] :
            if len(data) >= len(entry_list) :
                article = Article()
                article.set_params(id=data[0])
                self.article_list.append(article)
        return self.test_dataset

    def read_knowledgeable(self) :
        """ Read knowledgeable article.
        Each row of the file is a article.
        column[0] of the file is the id of the article.
        Each column[1:] of the file is the attributes of the article. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_classify_knowledgeable())
        for data in data_list :
            if len(data) >= 4 :
                article = Article()
                article.import_article(data)
                self.article_list.append(article)
        print 'reading keyword finished ...'
        self._constr_dict_id()

    def read_qa_article(self, rate=0.1) :
        """ Read simplified knowledgeable article.
        Each row of file is article.
        Each column of file is the attributes of the article. """
        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(self.path_manager.get_qa_articl())
        for data in data_list :
            if len(data) >= 4 :
                article = Article()
                article.import_article(data)
                self.article_list.append(article)
        print 'wrirting simply knowledgeable article finished ...'
        self._constr_dict_id()

    def read_keyword(self, keyword_path) :
        """ Read key_word from input/keyword.
        Each row of the file is a article.
        column[0] of the file is the id of the article.
        Each column[1:] of the file is the keyword of the article. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(keyword_path)
        for data in data_list :
            id = data[0]
            if id in self._id_article :
                self._id_article[id].import_keyword(data, length=100)
        print 'reading keyword finished ...'

    def read_sub_title(self, subtitle_path) :
        """ Read sub title of a article.
        Each row of the file is a sub title.
        column[0] of the file is the id of the article.
        column[1] of the file is the sub title. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(subtitle_path)
        for data in data_list :
            if len(data) >= 2 :
                id = data[0]
                if id in self._id_article :
                    self._id_article[id].import_sub_title(data)
        print 'reading sub title finished ...'

    def read_content_participle_sentence(self, sentence_path) :
        """ Read sub sentence of a article.
        Each row of the file is a sub sentence.
        column[0] of the file is the id of the article.
        column[1] of the file is the participle sentence. """

        self.file_operator = TextFileOperator()
        data_list = self.file_operator.reading(sentence_path)
        for data in data_list :
            if len(data) >= 2 :
                id = data[0]
                if id in self._id_article :
                    self._id_article[id].import_sub_sentence(data)
        print 'reading sub sentence finished ...'
    
    def feature_selecting(self, firpro_path='', secpro_path='', thrpro_path='', \
        word_path='', sp_path='', pc_path='', pos_path='') :
        """ select the feature. """
        selector = WordExtractor(firpro_path=firpro_path, secpro_path=secpro_path, \
            thrpro_path=thrpro_path, word_path=word_path)
        selector.extractFeature(self.article_list)
        selector = TokenExtractor(sp_path=sp_path, pc_path=pc_path)
        selector.extractFeature(self.article_list)
        selector = UserExtractor()
        selector.extractFeature(self.article_list)
        selector = PosExtractor(pos_path=pos_path)
        selector.extractFeature(self.article_list)
        print 'selecting feature finished ...'
    
    def classifying(self, seq=1) :
        """ Classify the article_list into knowledgeable and unknowledgeable.
        Return the sorted article_list and top of which is knowledgeable. """

        if seq == 1 :
            classifier = MultiConditionClassifier()
            self.sorted_article_list = classifier.sorting(self.article_list)
        elif seq == 2 :
            classifier = SvmClassifier()
            self.sorted_article_list = classifier.sorting( \
                self.train_dataset, self.train_label, self.article_list)
            self.write_support_vecotrs(classifier.support_index_list)
            self._gzh_sorting()
        elif seq == 'single_condition' :
            classifier = unspclf.SingleConditionClassifier()
            self.sorted_article_list = classifier.sorting(self.article_list)
        elif seq == 'train' :
            classifier = spclf.SvmClassifier()
            clf = classifier.training(self.train_dataset, self.train_label)
            classifier.storing(clf, path=clf_path)
        print 'classifying article_list finished ...'
    
    def title_simplifying(self, w2v_path='', spst_path='', seq=1) :
        """ Simplify the title of the article. """

        simplifier = TitleSimplifier(w2v_path=w2v_path, spst_path=spst_path)
        simplifier.model_simplifying(self.article_list)
        print 'simplifying title finished ...'

    def write_article_list(self, article_list, article_path='') :
        """ Write article list.
            Each row of file is article.
            Column[:] of the file is the attributes of the article.
        """
        file_operator = TextFileOperator()
        data_list = [['id', 'url', 'title', 'content']]
        for article in article_list :
            data_list.append([article.id, article.url, article.title, article.content])
        file_operator.writing(data_list, article_path)

    def write_knowledgeable_article(self, knowledge_path, num=10000) :
        """ Write knowledgeable article.
        Each row of file is article.
        Each column[0] of file is the id of the article. """
        file_operator = TextFileOperator()
        data_list = [['id', 'score']]
        sorted_article_list = sorted(self.article_list, key=lambda x: x.score, reverse=True)
        for article in sorted_article_list[0:num] :
            data_list.append([article.id, article.score])
        file_operator.writing(data_list, knowledge_path)

    def write_simply_article(self, simply_path) :
        """ Write simplified knowledgeable article.
        Each row of file is article.
        Each column of file is the attributes of the article. """
        self.file_operator = TextFileOperator()
        data_list = []
        for article in self.article_list :
            data_list.append(article.get_simply_article())
        self.file_operator.writing(data_list, simply_path)
        print 'wrirting knowledgeable article finished ...'

    def write_tag_list(self) :
        """ Write tag list of article.
        Each row of file is an article.
        Each column of file is the tags of the article. """
        self.file_operator = CSVFileOperator()
        data_list = []
        for article in self.article_list :
            data_list.append(article.get_tag_list())
        self.file_operator.writing(data_list, self.path_manager.get_tag_article_tag())
        print 'wrirting article tag_list finished ...'

    def write_support_vecotrs(self, support_index_list) :
        """ Write support vectors into a csv file.
        Each row of file is a support vector.
        Each column of file is the attributes of the support vector. """
        self.file_operator = CSVFileOperator()
        data_list = []
        for idx in support_index_list :
            data = []
            data.extend(self.article_list[idx].get_article())
            data.extend(self.article_list[idx].get_feature_set())
            data_list.append(data)
        self.file_operator.writing(data_list, self.path_manager.get_classify_supportvector())
        print 'wrirting support vectors finished ...'
                    
    def write_wordbag(self, wordbag, wordbag_path) :
        """ Write word bag.
            Each row of the file is a word.
            column[0] of the file is the word and feature.
        """
        file_operator = TextFileOperator()
        data_list = []
        for word in wordbag :
            data_list.append([word.to_string()])
        file_operator.writing(data_list, wordbag_path)

    def write_feature_list(self, feature_path) :
        """ Write feature list.
            Each row of the file is a article.
            column[0] of the file is the id.
            column[1:] of the file is the feature.
        """
        file_operator = TextFileOperator()
        data_list = [['id', 'url', 'title']]
        for name, value in self.article_list[0].feature_set :
            data_list[0].append(name)
        for article in self.article_list :
            data = [article.id, article.url, article.title]
            for name, value in article.feature_set :
                data.append(value)
            data_list.append(data)
        file_operator.writing(data_list, feature_path)

    def _constr_dict_id(self) :
        """ Construct id_article dict.
        key is id, value is Article object. """
        self._id_article = dict()
        for article in self.article_list :
            self._id_article[article.id] = article
        print 'constructing _id_article dict finished ...'

    def _constr_dict_index(self) :
        """ Construct id_index dict of article.
        key is id, value is index object. """
        self._id_index = dict()
        for index, article in enumerate(self.article_list) :
            self._id_index[article.id] = index
        print 'constructing _id_index dict finished ...'

    def _normalization(self, dataset) :
        """ Normalize dataset using mapminmax method. """
        normal_dataset = np.zeros(shape=(dataset.shape[0], dataset.shape[1]))
        for row in range(dataset.shape[0]) :
            for col in range(dataset.shape[1]) :
                normal_dataset[row, col] = dataset[row, col]
        for col in range(normal_dataset.shape[1]) :
            maximum = max(normal_dataset[:, col])
            minimum = min(normal_dataset[:, col])
            for row in range(normal_dataset.shape[0]) :
                if maximum - minimum == 0 :
                    normal_dataset[row, col] = 0.0
                else :
                    normal_dataset[row, col] = 1.0 * \
                        (maximum - normal_dataset[row, col]) / (maximum - minimum)
        return normal_dataset

    def _gzh_sorting(self) :
        """ Sort gzh by its article score and article number. """
        gzh_dict = dict()
        for article in self.article_list :
            gzh_id = article.id.split('_')[0]
            if gzh_id not in gzh_dict :
                gzh_dict[gzh_id] = []
            gzh_dict[gzh_id].append(article.score)
        gzh_list = []
        for gzh_id in gzh_dict :
            gzh_list.append([gzh_id, len(gzh_dict[gzh_id]), math.log(len(gzh_dict[gzh_id])) \
                * 1.0 * sum(gzh_dict[gzh_id]) / len(gzh_dict[gzh_id]), \
                1.0 * sum(gzh_dict[gzh_id]) / len(gzh_dict[gzh_id])])
        gzh_list = sorted(gzh_list, key=lambda x: x[2], reverse=True)
        for gzh_id, length, score, avg in gzh_list[-10:] :
            print gzh_id, length, score, avg

    def article_to_texts(self, choose='title') :
        """ Transform article to texts accordding to gensim. 
            Texts is a [list] and each element is a [list].
            Each element of the texts_list is a article.
            Each element of the article is a word.
            Like this [ [word_a, word_b, ...], 
                        [word_c, word_d, ...], 
                        ...
                      ]
        """
        remain_pos = [u'vn', u'nz', u'nt', u'ns', u'n', u'an']
        texts = []
        for article in self.article_list :
            text = []
            if choose == 'title' :
                text.extend([word.to_string() for word in article.participle_title if word.feature in remain_pos])
            elif choose == 'content' :
                text.extend([word.to_string() for word in article.participle_content if word.feature in remain_pos])
            elif choose == 'all' :
                text.extend([word.to_string() for word in article.participle_title if word.feature in remain_pos])
                text.extend([word.to_string() for word in article.participle_content if word.feature in remain_pos])
            texts.append(text)
        return texts
    
    def article_to_sentences(self) :
        """ Transform article to sentences accordding to gensim. 
            Sentences is a [list] and each element is a [list].
            Each element of the Sentences is a sentence.
            Each element of the sentence is a word.
            Like this [ [word_a, word_b, ...], 
                        [word_c, word_d, ...], 
                        ...
                      ]
        """
        sentences = []
        for article in self.article_list :
            for sentence in article.sub_sentence_list :
                if len(sentence) > 10 :
                    sentences.append([word.to_string() for word in sentence])
        return sentences