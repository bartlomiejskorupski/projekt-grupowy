from guizero import App, Box, Text, PushButton
from src.database.local_context import LocalContext
from env import DEBUG_BORDER
from src.misc.utils import addPadding

class HomeView:
  main_window = None
  db_context: LocalContext

  container: Box
  temperature_text: Text
  humidity_text: Text
  sound_text: Text

  def __init__(self, main_window):
    self.main_window = main_window
    self.db_context = self.main_window.db_context

    self.container = Box(
      self.main_window.app,
      layout='auto',
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    self.container.bg = '#222222'
    addPadding(self.container, 40)

    self.temperature_text = Text(
      self.container,
      text='Temp.: 0.0\u00B0C',
      size=40,
      align='top',
      width='fill',
      height='fill')
    self.humidity_text = Text(
      self.container,
      text='Humid.: 0.00%',
      size=40,
      align='top',
      width='fill',
      height='fill')
    self.sound_text = Text(
      self.container,
      text='Sound: 0.00dB',
      size=40,
      align='top',
      width='fill',
      height='fill')

  def update_reading_texts(self, temperature, humidity, sound):
    self.temperature_text.value = f'Temp.: {temperature:.2f}\u00B0C'
    self.humidity_text.value = f'Humid.: {humidity:.2f}%'
    self.sound_text.value = f'Sound: {sound:.2f}dB'
