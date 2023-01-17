import sqlite3
from env import DATA_FOLDER_PATH
import os
import logging as log
log.basicConfig(level=log.DEBUG)

class LocalContext:
  DB_FILENAME = 'data.db'

  def __init__(self):
    if not os.path.exists(DATA_FOLDER_PATH):
      log.info('Application data folder does not exist. Creating folder ' + DATA_FOLDER_PATH)
      os.mkdir(DATA_FOLDER_PATH)

    self.db_file_path = os.path.join(DATA_FOLDER_PATH, self.DB_FILENAME)
    self.connection = self.create_connection()
    self.create_reading_table()
    

  def create_connection(self):
    log.info('Connecting to database: ' + self.db_file_path)
    connection = None
    try:
      connection = sqlite3.connect(self.db_file_path)
    except sqlite3.Error as e:
      log.error(e)
    return connection

  def create_reading_table(self):
    log.info('Creating reading table')
    CREATE_READING_TABLE_SQL = """
      CREATE TABLE IF NOT EXISTS readings (
        id INT NOT NULL PRIMARY KEY,
        "date" DATETIME NOT NULL,
        value float NOT NULL
      );
    """
    try:
      cursor = self.connection.cursor()
      cursor.execute(CREATE_READING_TABLE_SQL)
    except sqlite3.Error as e:
      log.error(e)
