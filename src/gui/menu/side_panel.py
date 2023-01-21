from guizero import App, Box, PushButton, yesno, Text
from env import APP_VERSION, DEBUG_BORDER
from src.misc.utils import getTimeString, addPadding

class SidePanel:
  app: App
  container: Box
  exit_button: PushButton

  def __init__(self, app: App):
    self.app = app

    self.container = Box(
      app,
      layout='auto',
      align='left',
      height='fill',
      border=DEBUG_BORDER)
    self.container.bg = '#282828'

    addPadding(self.container, 20)

    self.version_text = Text(
      self.container,
      text=f'v{APP_VERSION}',
      align='bottom',
      size=8,
      color='grey')
    
    Box(self.container, layout='auto', align='bottom', width='fill', height=20)

    self.exit_button = PushButton(
      self.container,
      text='Exit',
      command=self.exit_button_click,
      align='bottom')
    self.exit_button.bg = 'red'

  def exit_button_click(self):
    if yesno('Exit', 'Are you sure you want to exit?'):
      self.app.destroy()
