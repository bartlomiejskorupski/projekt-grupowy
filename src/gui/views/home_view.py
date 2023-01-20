from datetime import datetime
from guizero import App, Box, Text, PushButton
from src.database.local_context import LocalContext
from env import DEBUG_BORDER
from src.model.reading import Reading
from src.misc.utils import addPadding
from src.sensor.sensor_reader import SensorReader

class HomeView:
  main_window = None
  sensor_reader: SensorReader
  db_context: LocalContext

  READING_DELAY = 1000

  container: Box
  temperature_text: Text
  humidity_text: Text
  sound_text: Text

  def __init__(self, main_window):
    self.main_window = main_window
    self.sensor_reader = SensorReader()
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
    self.container.repeat(self.READING_DELAY, function=self.update_temperature_and_humidity_text)

  def update_temperature_and_humidity_text(self):
    humidity, temperature = self.sensor_reader.getHumidityAndTemperatureReading()
    self.db_context.save_reading(Reading(datetime.now(), temperature))
    self.temperature_text.value = 'Temp.: {:.2f}\u00B0C'.format(temperature)
    self.humidity_text.value = 'Humid.: {:.2f}%'.format(humidity)

  def update_sound_text(self):
    reading = self.sensor_reader.getSoundReading()
    self.sound_text.value = 'Sound: {:.2f}dB'.format(reading)

