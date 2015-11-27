# -*- encoding = gb18030 -*-
""" Class word """


class Word :

    # methods
    def __init__(self, line) :
        if len(line.split(':')) == 1 :
            self.name = line
            self.feature = None
        elif len(line.split(':')) == 2 :
            self.name = line.split(':')[0]
            self.feature = line.split(':')[1]
        elif len(line.split(':')) > 2 :
            self.name = ''
            for part in line.split(':')[0:-2] :
                self.name += part + ':'
            self.name += line.split(':')[-2]
            self.feature = line.split(':')[-1]
        else :
            self.name = None
            self.feature = None

    def to_string(self) :
        name, feature = '', ''
        if self.name != None :
            name = self.name
        if self.feature != None :
            feature = self.feature
        return name + ':' + feature

    def set_params(self, **params) :
        """ Set parameters of the word. """
        for key, value in params.iteritems() :
            setattr(self, key, value)