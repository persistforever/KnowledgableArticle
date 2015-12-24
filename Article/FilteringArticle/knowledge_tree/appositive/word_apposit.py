# -*- encoding = gb18030 -*-

# package importing start
import gensim

from file.file_operator import TextFileOperator
# package importing end


class Appositive :

    def __init__(self) :
        pass

    def find_appositive(self, seeds, sentences) :
        """ Find appositive, seed is context, target is in sentences. """
        post_dict = dict((seed, dict()) for seed in seeds)
        prior_dict = dict()
        length = len(sentences) - 1
        for step, sentence in enumerate(sentences) :
            for idx, word in enumerate(sentence) :
                if word.name not in prior_dict :
                    prior_dict[word.name] = 0
                prior_dict[word.name] += 1
                for seed in seeds :
                    new_word = None
                    if (seed in word.name) and (len(seed) != len(word.name)) \
                        and (word.feature == u'n') :
                        if word.name.index(seed) == len(word.name) - 1 :
                            new_word = word.name[0:-1]
                    if seed == word.name and idx > 0 :
                        if sentence[idx-1].feature in [u'n', u't', u'b', u'd', u'nz'] :
                            new_word = sentence[idx-1].name
                    if new_word is not None :
                        if new_word not in post_dict[seed] :
                            post_dict[seed][new_word] = 0
                        post_dict[seed][new_word] += 1
            if step % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*step/length),
        print 'finish rate is %.2f%%\n' % (100.0*step/length)
        word_dict = dict()
        for seed in post_dict :
            post_sum = sum(post_dict[seed].values())
            for new_word in post_dict[seed] :
                word_dict[new_word + seed] = \
                    1.0 * prior_dict[seed] * post_dict[seed][new_word] / post_sum
        return word_dict