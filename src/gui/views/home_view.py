from guizero import App, Box, Text, PushButton
from env import DEBUG_BORDER
from src.misc.utils import addPadding
from src.sensor.sensor_reader import SensorReader

class HomeView:
  main_window = None
  sensor_reader: SensorReader

  READING_DELAY = 3000

  container: Box
  temperature_text: Text
  pressure_text: Text
  sound_text: Text

  def __init__(self, main_window):
    self.main_window = main_window
    self.sensor_reader = main_window.sensor_reader

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
    self.temperature_text.repeat(self.READING_DELAY, function=self.update_temperature_text)
    self.pressure_text = Text(
      self.container,
      text='Press.: 0.0kPa',
      size=40,
      align='top',
      width='fill',
      height='fill')
    self.pressure_text.repeat(self.READING_DELAY, function=self.update_pressure_text)
    self.sound_text = Text(
      self.container,
      text='Sound: 0.0dB',
      size=40,
      align='top',
      width='fill',
      height='fill')
    self.sound_text.repeat(self.READING_DELAY, function=self.update_sound_text)

  def update_temperature_text(self):
    reading = self.sensor_reader.getTemperatureReading()
    self.temperature_text.value = 'Temp.: {:.2f}\u00B0C'.format(reading)

  def update_pressure_text(self):
    reading = self.sensor_reader.getPressureReading()
    self.pressure_text.value = 'Press.: {:.2f}kPa'.format(reading)

  def update_sound_text(self):
    reading = self.sensor_reader.getSoundReading()
    self.sound_text.value = 'Sound: {:.2f}dB'.format(reading)

