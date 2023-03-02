import os

class ResourcePath:
  def __init__(self, relative_path: str):
      self.relative_path = relative_path

  def resource_path(self, file_name: str) -> str:
      '''return the path given the name of the file'''
      # import sys
      # if hasattr(sys, '_MEIPASS'):
      #   return os.path.join(sys._MEIPASS, self.relative_path + file_name)
      return os.path.join(os.path.abspath("."), self.relative_path + file_name)