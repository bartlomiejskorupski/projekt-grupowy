import sqlite3
import os
from env import DATA_FOLDER_PATH
from src.model.reading import Reading, ReadingType
from src.misc.utils import getDateTimeString
from datetime import datetime

import src.misc.logger as logger
LOG = logger.getLogger(__name__)


class LocalContext:
  DB_FILENAME = 'data.db'
  db_file_path: str
  connection: sqlite3.Connection

  DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

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
        id INTEGER PRIMARY KEY,
        "date" DATETIME NOT NULL,
        value REAL NOT NULL,
        "type" TEXT NOT NULL
      );
    """
    try:
      cursor = self.connection.cursor()
      cursor.execute(CREATE_READING_TABLE_SQL)
    except sqlite3.Error as e:
      LOG.error(e)
  
  def save_reading(self, reading: Reading) -> int:
    cur = self.connection.cursor()
    sql = 'INSERT INTO readings("date", value, "type") VALUES (?,?,?)'
    reading_date_text = reading.date.strftime('%Y-%m-%d %H:%M:%S.%f')
    cur.execute(sql, (reading_date_text, reading.value, reading.type.value))
    LOG.debug(f'Saving to db: date={reading_date_text}, value={reading.value}, type={reading.type.value}')
    self.connection.commit()
    return cur.lastrowid
  
  def fetch_readings(self, type: ReadingType, date_from: datetime, date_to: datetime):
    cur = self.connection.cursor()
    date_from_str = date_from.strftime(self.DATETIME_FORMAT)
    date_to_str = date_to.strftime(self.DATETIME_FORMAT)
    LOG.info(f'Fetching readings of type {type.value} and from {date_from_str} to {date_to_str}')
    sql = f'SELECT * FROM readings WHERE "type"="{type.value}" AND "date" BETWEEN "{date_from_str}" AND "{date_to_str}"'
    res = cur.execute(sql)
    readings = res.fetchall()
    LOG.info(f'Fetched {len(readings)} readings')
    return readings

  def fetch_all(self):
    cur = self.connection.cursor()
    LOG.info(f'Fetching all readings')
    sql = f'SELECT * FROM readings'
    res = cur.execute(sql)
    readings = res.fetchall()
    LOG.info(f'Fetched {len(readings)} readings')
    return readings
  
  def delete_reading(self, id: int):
    cur = self.connection.cursor()
    sql = 'DELETE FROM readings WHERE id=?'
    cur.execute(sql, (id,))
    self.connection.commit()


  def delete_readings(self, id_list: list[int]):
    tuples = list(map(lambda id: (id,), id_list))
    cur = self.connection.cursor()
    sql = 'DELETE FROM readings WHERE id=?'
    cur.executemany(sql, tuples)
    self.connection.commit()
    