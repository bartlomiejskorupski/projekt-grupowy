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
  sensor_reader: SensorReader

  top_panel: TopPanel
  side_panel: SidePanel
  home_view: HomeView

  READING_DELAY = 1000

  def __init__(self):
    self.app = App(
      title=APP_NAME,
      width=WINDOW_WIDTH,
      height=WINDOW_HEIGHT,
      layout='auto')
    self.app.font = 'Ubuntu'
    self.app.text_color = 'white'
    self.app.when_key_pressed = self.key_pressed
    self.app.when_closed

    self.db_context = LocalContext()
    self.sensor_reader = SensorReader()

    # init components
    LOG.debug('Initializing components')
    self.top_panel = TopPanel(self.app)
    Box(self.app,layout='auto',align='top',height=0,width='fill',border=True)
    self.side_panel = SidePanel(self.app)
    Box(self.app,layout='auto',align='left',height='fill',width=0,border=True)
    self.home_view = HomeView(self)

    self.app.repeat(self.READING_DELAY, self.read_sensors)

    LOG.debug('Application started')
    self.app.display()
  
  def read_sensors(self):
    humidity, temperature, = self.sensor_reader.getHumidityAndTemperatureReading()
    self.db_context.save_reading(Reading(datetime.now(), temperature))
    sound = self.sensor_reader.getSoundReading()
    self.home_view.update_reading_texts(temperature, humidity, sound)

  def key_pressed(self, event):
    if event.key == '\u001B':
      pass