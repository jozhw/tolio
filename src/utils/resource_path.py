'''resource_path.py - class methods to obtain relative path from file name'''
import os

class ResourcePath:
    '''This class takes a file name and returns the path'''

    def __init__(self, relative_path: str):
        '''Initialize the classes with relative_path of the file of interest'''
        self.relative_path = relative_path

    def resource_path(self, file_name: str) -> str:
        '''return the path given the name of the file'''
        # import sys
        # if hasattr(sys, '_MEIPASS'):
        #   return os.path.join(sys._MEIPASS, self.relative_path + file_name)
        return os.path.join(os.path.abspath("."), self.relative_path + file_name)