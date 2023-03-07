from guizero import App, Box, Text, Picture
from env import DEBUG_BORDER
from src.misc.utils import getTimeString, addPadding

class SidePanel:
  main_window = None
  app: App
  container: Box

  home_button: Picture
  settings_button: Picture
  humidity_button: Picture
  temperature_button: Picture
  sound_button: Picture

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

    self.home_button = Picture(
      self.container,
      image="src/images/home.png",
      align='top',
      width=40,
      height=40)
    self.home_button.when_clicked = self.home_button_click
    Box(self.container, layout='auto', align='top', width='fill', height=10, border=DEBUG_BORDER)
    self.settings_button = Picture(
      self.container,
      image="src/images/settings.png",
      align='top',
      width=40,
      height=40)
    self.settings_button.when_clicked = self.settings_button_click
    Box(self.container, layout='auto', align='top', width='fill', height=10, border=DEBUG_BORDER)
    self.temperature_button = Picture(
      self.container,
      image="src/images/temperature.png",
      align='top',
      width=40,
      height=40)
    self.temperature_button.when_clicked = self.temperature_button_click
    Box(self.container, layout='auto', align='top', width='fill', height=10, border=DEBUG_BORDER)
    self.humidity_button = Picture(
      self.container,
      image="src/images/humidity.png",
      align='top',
      width=40,
      height=40)
    self.humidity_button.when_clicked = self.humidity_button_click
    Box(self.container, layout='auto', align='top', width='fill', height=10, border=DEBUG_BORDER)
    self.sound_button = Picture(
      self.container,
      image="src/images/sound.png",
      align='top',
      width=40,
      height=40)
    self.sound_button.when_clicked = self.sound_button_click
    
  def home_button_click(self):
    self.clear_buttons_bg()
    self.home_button.bg = '#444444'
    self.main_window.home_button_click()
  
  def settings_button_click(self):
    self.clear_buttons_bg()
    self.settings_button.bg = '#444444'
    self.main_window.settings_button_click()

  def temperature_button_click(self):
    self.clear_buttons_bg()
    self.temperature_button.bg = '#444444'
    self.main_window.temperature_button_click()

  def humidity_button_click(self):
    self.clear_buttons_bg()
    self.humidity_button.bg = '#444444'
    self.main_window.humidity_button_click()

  def sound_button_click(self):
    self.clear_buttons_bg()
    self.sound_button.bg = '#444444'
    self.main_window.sound_button_click()

  def clear_buttons_bg(self):
    self.home_button.bg = '#282828'
    self.temperature_button.bg = '#282828'
    self.humidity_button.bg = '#282828'
    self.sound_button.bg = '#282828'
    self.settings_button.bg = '#282828'

