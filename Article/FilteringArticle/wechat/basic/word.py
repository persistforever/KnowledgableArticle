# -*- encoding = gb18030 -*-

# package importing start
# package importing end


class Word :

    # methods
    def __init__(self, line, sp_char=':') :
        self.name = ':'.join(line.split(sp_char)[0:-1])
        self.feature = line.split(sp_char)[-1]

    def set_params(self, **params) :
        """ Set parameters of the word. """
        for key, value in params.iteritems() :
            setattr(self, key, value)

    def to_string(self) :
        return self.name + '<:>' + self.feature