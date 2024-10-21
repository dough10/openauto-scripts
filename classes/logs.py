import logging
import logging.config
from datetime import datetime
class Logs:
  def __init__(self):
    self.__logger = logging.getLogger('')
    self.__logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('info.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    self.__logger.addHandler(file_handler)

  def get_logger(self):
    return self.__logger