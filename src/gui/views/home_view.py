from guizero import App, Box, Text, PushButton
from src.database.local_context import LocalContext
from env import DEBUG_BORDER
from src.misc.utils import addPadding

class HomeView:
  main_window = None
  db_context: LocalContext

  container: Box

  last_reading_box: Box
  temperature_text: Text
  humidity_text: Text
  sound_text: Text

  timer_box: Box
  status_text: Text
  timer = 0.0
  is_reading = False
  TIMER_UPDATE_DELAY = 100

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
      height=40,
      border=DEBUG_BORDER)
    self.status_text = Text(
      self.timer_box,
      text='Reading in: 5s',
      size=12,
      align='left',
      width='fill',
      height='fill')

    self.last_reading_box = Box(
      self.container,
      layout='auto',
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    self.temperature_text = Text(
      self.last_reading_box,
      text='Temp.: 0.0\u00B0C',
      size=20,
      align='top',
      width='fill',
      height='fill')
    self.humidity_text = Text(
      self.last_reading_box,
      text='Humid.: 0.00%',
      size=20,
      align='top',
      width='fill',
      height='fill')
    self.sound_text = Text(
      self.last_reading_box,
      text='Sound: 0.00dB',
      size=20,
      align='top',
      width='fill',
      height='fill')
    
    self.container.repeat(time=self.TIMER_UPDATE_DELAY, function=self.update_status)

  def update_reading_texts(self, temperature, humidity, sound, next_reading_in):
    self.temperature_text.value = f'Temp.: {temperature:.2f}\u00B0C'
    self.humidity_text.value = f'Humid.: {humidity:.2f}%'
    self.sound_text.value = f'Sound: {sound:.2f}dB'
    self.is_reading = False
    self.timer = next_reading_in
    self.status_text.text_color = 'white'

  def update_status(self):
    if self.is_reading:
      self.timer += self.TIMER_UPDATE_DELAY
      self.status_text.value = f'Reading... {self.timer/1000.0:0.1f}s'
    else:
      self.timer -= self.TIMER_UPDATE_DELAY
      self.status_text.value = f'Next reading in: {self.timer/1000.0:0.1f}s'

  def reading_started(self):
    self.is_reading = True
    self.timer = 0.0
    self.status_text.text_color = 'red'


