import threading
from guizero import App, Box, Text, PushButton
from env import APP_NAME, DEBUG_BORDER, WINDOW_WIDTH, WINDOW_HEIGHT
from src.model.reading import Reading
from src.sensor.sensor_reader import SensorReader
from src.gui.views.home_view import HomeView
from src.gui.menu.side_panel import SidePanel
from src.gui.menu.top_panel import TopPanel
from src.database.local_context import LocalContext
from src.misc.utils import addPadding
from datetime import datetime

import src.misc.logger as logger
LOG = logger.getLogger(__name__)

class MainWindow:
  app: App
  db_context: LocalContext
  sensor_thread: SensorReader

  top_panel: TopPanel
  side_panel: SidePanel
  home_view: HomeView

  READING_DELAY = 5

  def __init__(self):
    self.app = App(
      title=APP_NAME,
      width=WINDOW_WIDTH,
      height=WINDOW_HEIGHT,
      layout='auto')
    self.app.font = 'Ubuntu'
    self.app.text_color = 'white'
    self.app.when_key_pressed = self.key_pressed
    self.app.when_closed = self.close_app

    self.db_context = LocalContext()

    # init components
    LOG.debug('Initializing components')
    self.top_panel = TopPanel(self.app)
    Box(self.app,layout='auto',align='top',height=0,width='fill',border=True)
    self.side_panel = SidePanel(self)
    Box(self.app,layout='auto',align='left',height='fill',width=0,border=True)
    self.home_view = HomeView(self)

    self.sensor_thread = SensorReader(self.db_context, self.READING_DELAY)
    self.sensor_thread.reading_started = self.reading_started
    self.sensor_thread.reading_finished = self.reading_finished
    self.sensor_thread.start()

    self.app.display()
  
  def reading_started(self):
    LOG.debug('Reading started...')

  def reading_finished(self, temperature, humidity, sound):
    LOG.debug('Reading finished.')
    self.db_context.save_reading(Reading(datetime.now(), temperature))
    self.home_view.update_reading_texts(temperature, humidity, sound)
    

  def key_pressed(self, event):
    if event.key == '\u001B':
      pass
  
  def close_app(self):
    LOG.debug('Sensor thread stopping...')
    self.sensor_thread.stop()
    LOG.debug('App closing')
    self.app.destroy()

