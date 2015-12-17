# -*- encoding = gb18030 -*-

import jieba.posseg as pseg
import codecs


def read_sentences(sentence_path) :
	with codecs.open(sentence_path, 'r', 'gb18030') as fo :
		sentences = [line.strip().split('\t') for line in fo.readlines()]
	for sentence in sentences :
		words = pseg.cut(sentence[1])
		for word, flag in words :
			print word.encode('utf8'), flag


read_sentences('E:/data/knowledge/classify/fashion/debug/segmented_title')