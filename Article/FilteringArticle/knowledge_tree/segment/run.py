# -*- encoding = gb18030 -*-

# package importing start
import sys

from segment.segementor import TitleSegementor, ContentSegementor
from basic.word import Word
from file.file_operator import TextFileOperator
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, source_path, title_spst_path, content_spst_path, \
        sentence_path, seg_title_path, seg_content_path) :
        source_list = self.read_source_article(source_path)
        article_dict = self.constr_article_dict(source_list)
        title_segmentor = TitleSegementor(spst_path=title_spst_path)
        content_segmentor = ContentSegementor(spst_path=content_spst_path)
        sentences, article_dict = self.segment(article_dict, title_segmentor, content_segmentor)
        self.write_sentences(sentences, sentence_path)
        self.write_segmented_article(article_dict, seg_title_path, seg_content_path)

    def read_source_article(self, source_path) :
        """ Read source article.
            Each row is an article.
            Colunm[0] is the id of article.
            Column[1:] is the attributes of article.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(source_path)
        entry_list = data_list[0]
        source_list = []
        for data in data_list[1:] :
            if len(data) >= len(entry_list) :
                article = dict()
                article['id'] = data[0]
                article['url'] = data[1]
                article['pub_time'] = data[2]
                article['title'] = data[3]
                article['content'] = data[4]
                article['n_zan'] = data[5]
                article['n_forward'] = data[6]
                article['n_click'] = data[7]
                article['n_collect'] = data[8]
                article['read_time'] = data[9]
                article['finish_rate'] = data[10]
                source_list.append(article)
        return source_list

    def constr_article_dict(self, source_list) :
        """ Construct article dict.
            Key is id of article.
            Value is an article dict.
        """
        article_dict = dict()
        for article in source_list :
            key = article['id']
            if key not in article_dict :
                article_dict[key] = dict()
            for attr in article :
                article_dict[key][attr] = article[attr]
        return article_dict

    def segment(self, article_dict, title_segmentor, content_segmentor) :
        """ Segment title and content of article. """
        sentences = list()
        for id in article_dict :
            segmented_title = title_segmentor.segement(article_dict[id]['title'])
            article_dict[id]['segmented_title'] = segmented_title
            sentences.extend(segmented_title)
            segmented_content = content_segmentor.segement(article_dict[id]['content'])
            article_dict[id]['segmented_content'] = segmented_content
            sentences.extend(segmented_content)
        return sentences, article_dict

    def write_sentences(self, sentence_list, sentence_path) :
        """ Write sentences.
            Each row is a sentence.
        """
        file_operator = TextFileOperator()
        entry_list = ['sentence']
        data_list = list()
        data_list.append(entry_list)
        for sentence in sentence_list :
            data_list.append([sentence])
        file_operator.writing(data_list, sentence_path)

    def write_segmented_article(self, article_dict, seg_title_path, seg_content_path) :
        """ Write segmented title list.
            Each row is an sub title.
            Colunm[0] is the id of article.
            Column[1:] is the sub sentence of title.
            Write segmented content list.
            Each row is an sub content.
            Colunm[0] is the id of article.
            Column[1:] is the sub sentence of content.
        """
        file_operator = TextFileOperator()
        entry_list = ['id', 'segmented_title']
        data_list = list()
        data_list.append(entry_list)
        for id in article_dict :
            for sentence in article_dict[id]['segmented_title'] :
                data_list.append([id, sentence])
        file_operator.writing(data_list, seg_title_path)
        entry_list = ['id', 'segmented_content']
        data_list = list()
        data_list.append(entry_list)
        for id in article_dict :
            for sentence in article_dict[id]['segmented_content'] :
                data_list.append([id, sentence])
        file_operator.writing(data_list, seg_content_path)