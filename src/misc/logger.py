import logging
import os.path
from env import DATA_FOLDER_PATH
from datetime import datetime

dt_string = datetime.now().strftime('%Y%m%d_%H%M%S%f')

def getLogger(module_name: str) -> logging.Logger:
  ''' Configures and returns a logger for given module '''

  logger = logging.getLogger(module_name)
  logger.setLevel(logging.DEBUG)

  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.DEBUG)
  console_handler.setFormatter(formatter)
  logger.addHandler(console_handler)

  path = os.path.join(DATA_FOLDER_PATH, 'logs', dt_string + '.log')
  file_handler = logging.FileHandler(filename=path, encoding='utf-8')
  file_handler.setLevel(logging.DEBUG)
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)

  return logger
