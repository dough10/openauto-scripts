import os
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

# Fetch log level from the environment variable (default to 'WARNING')
log_level_str = os.getenv('LOG_LEVEL', 'WARNING').upper()

try:
  log_level = getattr(logging, log_level_str)
except AttributeError:
  raise ValueError(f"Invalid log level: {log_level_str}. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL.")

class Logs:
  """
  A class that sets up logging for the application.
  
  This class provides a logging setup with rotating log files and console output.
  The log level can be configured via an environment variable, and it defaults to 'WARNING'.
  It supports log rotation to prevent log files from becoming too large.
  """
  def __init__(self, max_bytes: int = 5_000_000, backup_count: int = 5) -> None:
    """
    Initializes the logger and sets up log rotation and console output.
    
    Args:
      max_bytes (int): The maximum size of the log file before it rotates (in bytes). Default is 5 MB.
      backup_count (int): The number of backup log files to keep. Default is 5.
    """ 
    self.__logger = logging.getLogger('openauto-scripts')
    self.__logger.setLevel(log_level)

    if not self.__logger.hasHandlers():
      # Create a rotating file handler
      file_handler = RotatingFileHandler('openauto-scripts.log', maxBytes=max_bytes, backupCount=backup_count)
      formatter = logging.Formatter('%(asctime)s %(filename)s:%(levelname)s - %(message)s')
      file_handler.setFormatter(formatter)
      self.__logger.addHandler(file_handler)

      # Create a stream handler for console output
      stream_handler = logging.StreamHandler()
      stream_handler.setFormatter(formatter)
      self.__logger.addHandler(stream_handler)

      self.__logger.info(f"Log level set to: {log_level_str}")

  def get_logger(self) -> logging:
    """
    Returns the logger instance.
    
    Returns:
      logging: The logger instance configured with file and console handlers.
    """
    return self.__logger

# Example usage
if __name__ == "__main__":
  log = Logs()
  logger = log.get_logger()
  logger.debug("This is a debug message")
  logger.info("This is an info message")
  logger.warning("This is a warning message")
