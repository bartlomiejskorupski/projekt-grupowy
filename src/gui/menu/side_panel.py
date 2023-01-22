from guizero import App, Box, PushButton, yesno, Text
from env import APP_VERSION, DEBUG_BORDER
from src.misc.utils import getTimeString, addPadding

class SidePanel:
  main_window = None
  app: App
  container: Box
  exit_button: PushButton

  def __init__(self, main_window):
    self.main_window = main_window
    self.app = self.main_window.app

    self.container = Box(
      self.app,
      layout='auto',
      align='left',
      height='fill',
      border=DEBUG_BORDER)
    self.container.bg = '#282828'

    addPadding(self.container, 8)

    self.version_text = Text(
      self.container,
      text=f'v{APP_VERSION}',
      align='bottom',
      size=6,
      color='grey')
    
    Box(self.container, layout='auto', align='bottom', width='fill', height=10, border=DEBUG_BORDER)

    self.exit_button = PushButton(
      self.container,
      text='Exit',
      command=self.exit_button_click,
      align='bottom')
    self.exit_button.bg = 'red'

  def exit_button_click(self):
    if yesno('Exit', 'Are you sure you want to exit?'):
      self.main_window.close_app()
