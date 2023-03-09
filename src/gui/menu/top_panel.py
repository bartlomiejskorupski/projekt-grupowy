from guizero import App, Text, Box, PushButton, Picture, yesno
from env import APP_NAME, DEBUG_BORDER, APP_VERSION
from src.misc.utils import getTimeString, addPadding
from os import path, getcwd

class TopPanel:
  main_window = None
  app: App
  container: Box
  title_text: Text
  time_text: Text

  exit_button: Picture

  def __init__(self, main_window):
    self.main_window = main_window
    self.app = self.main_window.app

    self.container = Box(
      self.app,
      layout='auto',
      align='top',
      width='fill',
      border=DEBUG_BORDER)
    self.container.bg = '#282828'

    addPadding(self.container, 8)
    
    self.title_text = Text(
      self.container,
      text=APP_NAME,
      align='left',
      size=16)
    
    Text(
      self.container,
      text=f'  v{APP_VERSION}',
      align='left',
      size=8,
      color='grey')

    self.exit_button = Picture(
      self.container,
      image=path.join(getcwd(), 'src/images/exit.png'),
      align='right',
      width=24,
      height=24)
    self.exit_button.when_clicked = self.exit_button_click

    Box(self.container, layout='auto', align='right', width=10, height='fill', border=DEBUG_BORDER)

    self.time_text = Text(
      self.container,
      text=getTimeString(),
      align='right',
      size=10)
    self.time_text.repeat(1000,
      function=self.update_clock)

  def update_clock(self):
    current_time_string = getTimeString()
    if self.time_text.value != current_time_string:
      self.time_text.value = current_time_string

  def exit_button_click(self):
    if yesno('Exit', 'Are you sure you want to exit?'):
      self.main_window.close_app()

