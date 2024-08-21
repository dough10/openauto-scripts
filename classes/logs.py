import json
import logging
import logging.config

class Logs:
  def __init__(self):
    self.__logger = logging.getLogger('openauto pro scripts')
    # with open('config.json', 'r') as con_in:
    #   config = json.load(con_in)
    logging.basicConfig(filename='info.log', level=logging.INFO)
    # logging.config.dictConfig(config)
    
  def get_logger(self):
    return self.__logger