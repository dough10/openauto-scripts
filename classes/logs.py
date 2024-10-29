import os
import logging
import logging.config
from logging.handlers import RotatingFileHandler

class Logs:
  def __init__(self, filename: str, level: int = logging.DEBUG, max_bytes: int = 5_000_000, backup_count: int = 5):
    self.__logger = logging.getLogger('openauto-scripts')
    self.__logger.setLevel(level)

    if not self.__logger.handlers:
      file_handler = RotatingFileHandler(f'{os.path.basename(filename)}.log', maxBytes=max_bytes, backupCount=backup_count)
      formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
      file_handler.setFormatter(formatter)
      self.__logger.addHandler(file_handler)

      stream_handler = logging.StreamHandler()
      stream_handler.setFormatter(formatter)
      self.__logger.addHandler(stream_handler)

  def get_logger(self):
    return self.__logger
