from guizero import App, Box, Text, PushButton
from env import APP_NAME, DEBUG_BORDER
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
  WIDTH = 1000
  HEIGHT = 1000

  app: App
  db_context: LocalContext

  top_panel: TopPanel
  side_panel: SidePanel
  home_view: HomeView

  def __init__(self):
    self.app = App(
      title=APP_NAME,
      width=self.WIDTH,
      height=self.HEIGHT,
      layout='auto')
    self.app.font = 'Ubuntu'
    #self.app.bg = 'skyblue'
    self.app.text_color = 'white'
    self.app.when_key_pressed = self.key_pressed
    self.app.when_closed

    self.db_context = LocalContext()

    # init components
    LOG.debug('Initializing components')
    self.top_panel = TopPanel(self.app)
    # Horizontal line
    Box(self.app,layout='auto',align='top',height=0,width='fill',border=True)
    self.side_panel = SidePanel(self.app)
    # Vertical line
    Box(self.app,layout='auto',align='left',height='fill',width=0,border=True)

    self.home_view = HomeView(self)

    LOG.debug('Application started')
    self.app.display()
  
  def key_pressed(self, event):
    if event.key == '\u001B':
      pass