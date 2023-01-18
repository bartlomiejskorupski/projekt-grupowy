import logging
from os.path import join
from env import DATA_FOLDER_PATH

def getLogger(module_name):
  logger = logging.getLogger(module_name)
  logger.setLevel(logging.DEBUG)

  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.DEBUG)
  console_handler.setFormatter(formatter)
  logger.addHandler(console_handler)

  path = join(DATA_FOLDER_PATH, 'logs.txt')
  file_handler = logging.FileHandler(filename=path, encoding='utf-8')
  file_handler.setLevel(logging.DEBUG)
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)

  return logger
