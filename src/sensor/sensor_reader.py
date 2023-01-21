from datetime import datetime
from threading import Thread, Event
from typing import Callable
from src.database.local_context import LocalContext
from src.model.reading import Reading
import src.misc.logger as logger
LOG = logger.getLogger(__name__)

try:
  import Adafruit_DHT as DHT
except ModuleNotFoundError:
  LOG.warning('Adafruit_DHT module not found! Using fake one.')
  import src.misc.fake_dht as DHT

class SensorReader(Thread):
  running: bool
  e: Event
  db_context: LocalContext
  reading_delay: float

  reading_started: Callable[[], None] = None
  reading_finished: Callable[[float, float, float], None] = None

  def __init__(self, db_context: LocalContext, reading_delay: float):
    """ reading_delay - time between readings in seconds """
    Thread.__init__(self)
    self.daemon = True
    self.sensor = DHT.DHT22
    self.pin = 4
    self.running = True
    self.e = Event()
    self.db_context = db_context
    self.reading_delay = reading_delay

  def run(self):
    while True:
      if self.reading_started:
        self.reading_started()
      humidity, temperature = self.getHumidityAndTemperatureReading()
      sound = self.getSoundReading()
      if self.reading_finished:
        self.reading_finished(temperature, humidity, sound)
      LOG.debug(f'WAIT {self.reading_delay}')
      self.e.wait(self.reading_delay)
      if not self.running:
        break
    LOG.debug('Sensor thread stopped.')

  def stop(self):
    self.running = False
    self.e.set()

  def getHumidityAndTemperatureReading(self) -> tuple[float, float]:
    # read_retry takes anywhere from 0 to 30 seconds to complete
    _, temp = DHT.read_retry(self.sensor,self.pin)
    return (0.0, temp)

  def getSoundReading(self) -> float:
    # TODO: Implement method
    return 0.0
