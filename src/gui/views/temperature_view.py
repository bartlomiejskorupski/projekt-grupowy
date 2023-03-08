from guizero import Box, Text, PushButton
from src.database.local_context import LocalContext
from env import DEBUG_BORDER
from src.misc.utils import addPadding
from src.model.reading import ReadingType
from datetime import datetime, timedelta

import src.misc.logger as logger
LOG = logger.getLogger(__name__)

class TemperatureView:
  main_window = None
  db_context: LocalContext
  container: Box
  
  def __init__(self, main_window):
    self.main_window = main_window
    self.db_context = self.main_window.db_context

    self.container = Box(
      self.main_window.app,
      layout='auto',
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    self.container.bg = '#222222'
    addPadding(self.container, 10)

    Text(
      self.container,
      align='top',
      width='fill',
      text='Temperature',
      size=10)
    
    debug_button = PushButton(
      self.container,
      align='bottom',
      text='debug',
      command=self.debug_button_click)
    
  def debug_button_click(self):
    date_from = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=1)
    date_to = datetime.now().replace(hour=23, minute=59, second=59)
    readings = self.db_context.fetch_readings(ReadingType.TEMPERATURE, date_from, date_to)
    #readings = self.db_context.fetch_all()


