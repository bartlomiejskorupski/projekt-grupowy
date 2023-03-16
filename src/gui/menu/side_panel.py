from guizero import App, Box, PushButton
from env import DEBUG_BORDER, PROJECT_PATH
from src.misc.utils import addPadding
from os import path

class SidePanel:
  '''
  Side panel containing buttons for routing between views.
  '''

  main_window = None
  app: App
  container: Box

  home_button: PushButton
  settings_button: PushButton
  humidity_button: PushButton
  temperature_button: PushButton
  sound_button: PushButton

  BG_COLOR = '#282828'
  HIGHLIGHTED_COLOR = '#444444'

  IMAGE_SIZE = 36

  def __init__(self, main_window):
    self.main_window = main_window
    self.app = self.main_window.app

    self.container = Box(
      self.app,
      layout='auto',
      align='left',
      height='fill',
      border=DEBUG_BORDER)
    self.container.bg = self.BG_COLOR

    addPadding(self.container, 6)

    self.home_button = PushButton(
      self.container,
      image=path.join(PROJECT_PATH, 'src/images/home.png'),
      align='top',
      width=self.IMAGE_SIZE,
      height=self.IMAGE_SIZE,
      command=self.home_button_click)
    
    Box(self.container, layout='auto', align='top', width='fill', height=10, border=DEBUG_BORDER)
    self.settings_button = PushButton(
      self.container,
      image=path.join(PROJECT_PATH, 'src/images/settings.png'),
      align='top',
      width=self.IMAGE_SIZE,
      height=self.IMAGE_SIZE,
      command=self.settings_button_click)
    Box(self.container, layout='auto', align='top', width='fill', height=10, border=DEBUG_BORDER)
    self.temperature_button = PushButton(
      self.container,
      image=path.join(PROJECT_PATH, "src/images/temperature.png"),
      align='top',
      width=self.IMAGE_SIZE,
      height=self.IMAGE_SIZE,
      command=self.temperature_button_click)
    Box(self.container, layout='auto', align='top', width='fill', height=10, border=DEBUG_BORDER)
    self.humidity_button = PushButton(
      self.container,
      image=path.join(PROJECT_PATH, "src/images/humidity.png"),
      align='top',
      width=self.IMAGE_SIZE,
      height=self.IMAGE_SIZE,
      command=self.humidity_button_click)
    Box(self.container, layout='auto', align='top', width='fill', height=10, border=DEBUG_BORDER)
    self.sound_button = PushButton(
      self.container,
      image=path.join(PROJECT_PATH, "src/images/sound.png"),
      align='top',
      width=self.IMAGE_SIZE,
      height=self.IMAGE_SIZE,
      command=self.sound_button_click)
    
  def home_button_click(self):
    self.clear_buttons_bg()
    self.home_button.bg = self.HIGHLIGHTED_COLOR
    self.main_window.home_button_click()
  
  def settings_button_click(self):
    self.clear_buttons_bg()
    self.settings_button.bg = self.HIGHLIGHTED_COLOR
    self.main_window.settings_button_click()

  def temperature_button_click(self):
    self.clear_buttons_bg()
    self.temperature_button.bg = self.HIGHLIGHTED_COLOR
    self.main_window.temperature_button_click()

  def humidity_button_click(self):
    self.clear_buttons_bg()
    self.humidity_button.bg = self.HIGHLIGHTED_COLOR
    self.main_window.humidity_button_click()

  def sound_button_click(self):
    self.clear_buttons_bg()
    self.sound_button.bg = self.HIGHLIGHTED_COLOR
    self.main_window.sound_button_click()

  def clear_buttons_bg(self):
    self.home_button.bg = self.BG_COLOR
    self.temperature_button.bg = self.BG_COLOR
    self.humidity_button.bg = self.BG_COLOR
    self.sound_button.bg = self.BG_COLOR
    self.settings_button.bg = self.BG_COLOR

