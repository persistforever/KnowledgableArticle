# -*- encoding = gb18030 -*-
""" Manager of project's global path """

import os
import ConfigParser


class PathManager :

    def __init__(self) :
        self.project_dir = os.path.abspath('E:/file/knowledge/')
        self._get_configuration()

    def _get_configuration(self) :
        """ Get basic configuration of path manager. """
        _cfg = ConfigParser.ConfigParser()
        _cfg.read(self.get_tools_config())
        self.type = _cfg.get('corpus', 'type')
        self.date = _cfg.get('corpus', 'date')
    
    def get_classify_traindataset(self) :
        path = os.path.abspath(self.project_dir) 
        path = os.path.join(path, 'train', self.type, 'traindataset')
        return path
    
    def get_classify_article(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'classify', self.type, self.date, 'article')
        return path
    
    def get_classify_keyword(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'classify', self.type, self.date, 'keyword')
        return path
    
    def get_classify_testdataset(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'classify', self.type, self.date, 'testdataset')
        return path
    
    def get_classify_knowledgable(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'classify', self.type, self.date, 'knowledgeable')
        return path
    
    def get_tag_wordtopic(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'tag', self.type, 'wordtopic')
        return path
    
    def get_tag_articletopic(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'tag', self.type, 'articletopic')
        return path
    
    def get_tag_wordbag(self) :
        path = os.path.abspath(self.project_dir) 
        path = os.path.join(path, 'tag', self.type, 'wordbag')
        return path
    
    def get_tag_bagofword(self) :
        path = os.path.abspath(self.project_dir) 
        path = os.path.join(path, 'tag', self.type, 'bagofword')
        return path
    
    def get_tag_tagtree(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'tag', self.type, 'tagtree')
        return path
    
    def get_tag_taglist(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'tag', self.type, 'taglist')
        return path
    
    def get_tag_article_tag(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'tag', self.type, 'articletag')
        return path
    
    def get_tools_vector(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'tools', 'vectors.txt')
        return path
    
    def get_tools_config(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'tools', 'configuration.ini')
        return path