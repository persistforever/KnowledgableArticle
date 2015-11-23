# -*- encoding = gb18030 -*-
""" Class word """


class Word :
    # attributes
    name = ''
    feature = ''

    # methods
    def __init__(self, line) :
        if len(line.split(':')) == 1 :
            self.name = line
            self.feature = None
        elif len(line.split(':')) == 2 :
            self.name = line.split(':')[0]
            self.feature = line.split(':')[1]
        else :
            self.name = None
            self.feature = None


    def toString(self) :
        return self.name + ':' + self.feature