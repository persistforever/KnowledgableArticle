# -*- encoding = gb18030 -*-
'''
Basic module 
	Word class
'''


class Word :
    # attributes
    name = ''
    feature = ''

    # methods
    def __init__(self, line) :
        if len(line.split(':')) == 2 :
            self.name = line.split(':')[0]
            self.feature = line.split(':')[1]

    def toString(self) :
        return self.name + ':' + self.feature