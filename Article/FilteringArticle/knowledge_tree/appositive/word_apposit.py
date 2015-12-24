# -*- encoding = gb18030 -*-

# package importing start
import gensim

from file.file_operator import TextFileOperator
# package importing end


class Appositive :

    def __init__(self) :
        pass

    def find_appositive(self, seed, sentences) :
        """ Find appositive, seed is context, target is in sentences. """
        word_dict = dict()
        for sentence in sentences :
            for idx, word in enumerate(sentence) :
                new_word = None
                if (seed in word.name) and (len(seed) != len(word.name)) :
                    if word.name.index(seed) == len(word.name) - 1 :
                        new_word = word.name
                if seed == word.name and idx > 0 :
                    new_word = sentence[idx-1].name + word.name
                if new_word is not None :
                    if new_word not in word_dict :
                        word_dict[new_word] = 0
                    word_dict[new_word] += 1
        return word_dict