from guizero import App, Text, Box, PushButton
from env import APP_NAME, DEBUG_BORDER
from src.misc.utils import getTimeString, addPadding

class TopPanel:
  app: App
  container: Box
  title_text: Text
  time_text: Text

  def __init__(self, app: App):
    self.app = app

    self.container = Box(
      app,
      layout='auto',
      align='top',
      width='fill',
      border=DEBUG_BORDER)
    self.container.bg = '#282828'

    addPadding(self.container, 20)
    
    self.title_text = Text(
      self.container,
      text=APP_NAME,
      align='left',
      size=26)

    self.time_text = Text(
      self.container,
      text=getTimeString(),
      align='right',
      size=16)
    self.time_text.repeat(100,
      function=self.update_clock)

  def update_clock(self):
    self.time_text.value = getTimeString()

