# -*- encoding = gb18030 -*-
""" Manager of project's global path """

import os
import ConfigParser


class PathManager :

    def __init__(self) :
        self.project_dir = os.path.abspath('E:/file/knowledgable/')
        self.config_dir = os.path.join(self.project_dir, 'global', 'configuration.ini')
        self.get_configuration(self.config_dir)

    def get_configuration(self, config_path) :
        """ Get basic configuration of path manager. """
        _cfg = ConfigParser.ConfigParser()
        _cfg.read(config_path)
        self.type = _cfg.get('corpus', 'type')
        self.date = _cfg.get('corpus', 'date')

    def get_input_article(self) :
        path = os.path.abspath(self.project_dir) 
        path = os.path.join(path, 'input', self.type, self.date, 'article')
        return path
    
    def get_input_info(self, type, date) :
        path = os.path.abspath(self.project_dir) 
        path = os.path.join(path, 'input', type, date, 'info')
        return path
    
    def get_input_traindataset(self) :
        path = os.path.abspath(self.project_dir) 
        path = os.path.join(path, 'input', self.type, 'traindataset')
        return path
    
    def get_input_wordbag(self) :
        path = os.path.abspath(self.project_dir) 
        path = os.path.join(path, 'input', self.type, 'wordbag')
        return path
    
    def get_output_origindata(self) :
        path = os.path.abspath(self.project_dir) 
        path = os.path.join(path, 'output', self.type, self.date, 'origindata')
        return path
    
    def get_output_article(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'output', self.type, self.date, 'article')
        return path
    
    def get_output_info(self, type, date) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'output', type, date, 'info')
        return path
    
    def get_output_split(self, type, date) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'output', type, date, 'split')
        return path
    
    def get_output_keyword(self, type, date) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'output', type, date, 'keyword')
        return path
    
    def get_output_keywordTitle(self, type, date) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'output', type, date, 'keyword_title')
        return path
    
    def get_output_testdataset(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'output', self.type, self.date, 'testdataset')
        return path
    
    def get_output_knowledgable(self) :
        path = os.path.abspath(self.project_dir)
        path = os.path.join(path, 'output', self.type, self.date, 'knowledgeable')
        return path