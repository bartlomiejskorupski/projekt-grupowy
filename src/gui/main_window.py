from guizero import App, Box, Text, PushButton
from src.database.local_context import LocalContext
from src.misc.utils import addPadding
from datetime import datetime

import src.misc.logger as logger
LOG = logger.getLogger(__name__)

class MainWindow:
  TITLE = 'Projekt Grupowy'
  WIDTH = 1000
  HEIGHT = 1000

  def __init__(self):
    self.app = App(
      title=self.TITLE,
      width=self.WIDTH,
      height=self.HEIGHT,
      layout='auto')
    self.app.font = 'Ubuntu'
    self.app.bg = 'skyblue'
    self.app.text_color = 'black'
    self.app.when_key_pressed = self.key_pressed
    self.app.when_closed

    # init components
    LOG.debug('Initializing components')

    self.init_top_panel()

    self.bottom_box = Box(
      self.app,
      layout='auto',
      align='top',
      width='fill',
      height='fill')

    self.db_context = LocalContext()

    LOG.debug('Application started')
    self.app.display()
  
  def init_top_panel(self):
    self.top_panel = Box(
      self.app,
      layout='auto',
      align='top',
      width='fill')

    addPadding(box=self.top_panel, padding=20, debug_border=True)

    Text(
      self.top_panel,
      text='Sensor 3000',
      align='left',
      size=26)

    Box(self.top_panel, align='left', height='fill', width='20', border=2)

    time_text = Text(
      self.top_panel,
      text='',
      align='left',
      size=16)
    self.update_clock(time_text)
    time_text.repeat(1000, function=self.update_clock, args=[time_text])

    exit_button = PushButton(self.top_panel,text='Close' ,command=self.exit_button_click, align='right', height='fill')
    exit_button.bg = 'lightgrey'


  def key_pressed(self, event):
    if event.key == '\u001B':
      pass

  def exit_button_click(self):
    self.app.destroy()

  def update_clock(self, time_text: Text):
    time_text.value = datetime.now().strftime('%H:%M:%S')
