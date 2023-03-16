from guizero import App, Box, Text, PushButton
from src.database.local_context import LocalContext
from env import DEBUG_BORDER
from src.misc.utils import addPadding
from math import floor

import src.misc.logger as logger
LOG = logger.getLogger(__name__)

class HomeView:
  '''
  Home view containing last reading data and time until next reading
  '''

  main_window = None
  db_context: LocalContext

  container: Box

  temperature_box: Box
  humidity_box: Box
  sound_box: Box

  temperature_text: Text
  humidity_text: Text
  sound_text: Text

  timer_box: Box
  status_text: Text
  timer = 0.0
  is_reading = False
  TIMER_UPDATE_DELAY = 100

  HEADER_TEXT_SIZE = 16
  HEADER_TEXT_WIDTH = 160
  READING_TEXT_SIZE = 20

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
    addPadding(self.container, 10)

    self.timer_box = Box(
      self.container,
      layout='auto',
      align='top',
      width='fill',
      border=DEBUG_BORDER)
    self.status_text = Text(
      self.timer_box,
      text='',
      size=8,
      align='left')
    
    self.temperature_box = Box(
      self.container,
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    
    temperature_header_box = Box(
      self.temperature_box,
      align='left',
      width=self.HEADER_TEXT_WIDTH,
      height='fill',
      border=DEBUG_BORDER)

    Text(
      temperature_header_box,
      align='right',
      text='Temperature:',
      size=self.HEADER_TEXT_SIZE)
    
    self.temperature_text = Text(
      self.temperature_box,
      text='',
      size=self.READING_TEXT_SIZE,
      align='top',
      width='fill',
      height='fill')
    
    self.humidity_box = Box(
      self.container,
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    humidity_header_box = Box(
      self.humidity_box,
      align='left',
      width=self.HEADER_TEXT_WIDTH,
      height='fill',
      border=DEBUG_BORDER)
    
    Text(
      humidity_header_box,
      align='right',
      text='Humidity:',
      size=self.HEADER_TEXT_SIZE)

    self.humidity_text = Text(
      self.humidity_box,
      text='',
      size=self.READING_TEXT_SIZE,
      align='left',
      width='fill',
      height='fill')
    
    self.sound_box = Box(
      self.container,
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    
    sound_header_box = Box(
      self.sound_box,
      align='left',
      width=self.HEADER_TEXT_WIDTH,
      height='fill',
      border=DEBUG_BORDER)

    Text(
      sound_header_box,
      align='right',
      text='Sound:',
      size=self.HEADER_TEXT_SIZE)

    self.sound_text = Text(
      self.sound_box,
      text='',
      size=self.READING_TEXT_SIZE,
      align='left',
      width='fill',
      height='fill')
    
    self.container.repeat(time=self.TIMER_UPDATE_DELAY, function=self.update_status)

  def update_reading_texts(self, temperature, humidity, sound, next_reading_in):
    if temperature is not None:
      self.temperature_text.value = f'{temperature:.2f}\u00B0C'
    self.humidity_text.value = f'{humidity:.2f}%'
    self.sound_text.value = f'{sound:.2f}dB'
    self.is_reading = False
    self.timer = next_reading_in
    self.status_text.text_color = 'white'

  def update_status(self):
    if self.is_reading:
      self.timer += self.TIMER_UPDATE_DELAY
      all_seconds = floor(self.timer/1000.0)
      status_text = f'Reading... {all_seconds}s'
    else:
      self.timer -= self.TIMER_UPDATE_DELAY
      all_seconds = floor(self.timer/1000.0)
      minutes = floor(all_seconds/60.0)
      seconds = all_seconds % 60
      status_text = f'Next reading in: {minutes}:{seconds:02d}'
    if self.status_text.value != status_text:
      self.status_text.value = status_text

  def reading_started(self):
    self.is_reading = True
    self.timer = 0.0
    self.status_text.text_color = 'red'


