# -*- encoding = gb18030 -*-

# package importing start
# package importing end


class Word :

    # methods
    def __init__(self, line, sp_char=':') :
        if len(line.split(sp_char)) > 1 :
            self.name = ':'.join(line.split(sp_char)[0:-1])
            self.feature = line.split(sp_char)[-1]
        else :
            self.name = line.split(sp_char)[0]
            self.feature = None

    def set_params(self, **params) :
        """ Set parameters of the word. """
        for key, value in params.iteritems() :
            setattr(self, key, value)

    def to_string(self) :
        if self.feature == None :
            return self.name + '<:>'
        else :
            return self.name + '<:>' + self.feature