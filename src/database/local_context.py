import sqlite3
import os
from env import DATA_FOLDER_PATH
from src.model.reading import Reading

import src.misc.logger as logger
LOG = logger.getLogger(__name__)


class LocalContext:
  DB_FILENAME = 'data.db'
  db_file_path: str
  connection: sqlite3.Connection

  def __init__(self):
    if not os.path.exists(DATA_FOLDER_PATH):
      LOG.info('Application data folder does not exist. Creating ' + DATA_FOLDER_PATH)
      os.mkdir(DATA_FOLDER_PATH)

    self.db_file_path = os.path.join(DATA_FOLDER_PATH, self.DB_FILENAME)
    self.connection = self.create_connection()
    self.create_reading_table()
  
  def __del__(self):
    LOG.info('Closing database connection')
    self.connection.close()

  def create_connection(self) -> sqlite3.Connection:
    LOG.info('Connecting to database: ' + self.db_file_path)
    connection = None
    try:
      # check_same_thread=False - ghetto workaround for threading problems
      connection = sqlite3.connect(self.db_file_path, check_same_thread=True)
    except sqlite3.Error as e:
      LOG.error(e)
    return connection

  def create_reading_table(self):
    LOG.debug('Creating reading table')
    CREATE_READING_TABLE_SQL = """
      CREATE TABLE IF NOT EXISTS readings (
        id integer PRIMARY KEY,
        "date" DATETIME NOT NULL,
        value float NOT NULL
      );
    """
    try:
      cursor = self.connection.cursor()
      cursor.execute(CREATE_READING_TABLE_SQL)
    except sqlite3.Error as e:
      LOG.error(e)
  
  def save_reading(self, reading: Reading) -> int:
    sql = 'INSERT INTO readings("date", value) VALUES (?,?)'
    # LOG.debug('Executing query ' + sql + ' with ' + str(reading))
    cur = self.connection.cursor()
    cur.execute(sql, (reading.date.strftime('%Y-%m-%d %H:%M:%S.%f'), reading.value))
    self.connection.commit()
    return cur.lastrowid

