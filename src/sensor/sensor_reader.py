from datetime import datetime
from queue import Queue
from threading import Thread, Event
from typing import Callable
from src.model.app_event import AppEvent, AppEventType
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
  reading_delay: float

  event_queue: Queue[AppEvent]

  def __init__(self, event_queue: Queue, reading_delay: float):
    """ reading_delay - time between readings in seconds """
    Thread.__init__(self)
    self.daemon = True
    self.sensor = DHT.DHT22
    self.pin = 4
    self.running = True
    self.e = Event()
    self.event_queue = event_queue
    self.reading_delay = reading_delay

  def run(self):
    while True:
      self.event_queue.put(AppEvent(AppEventType.SENSOR_READING_STARTED, {}))

      humidity, temperature = self.getHumidityAndTemperatureReading()
      sound = self.getSoundReading()

      self.event_queue.put(AppEvent(AppEventType.SENSOR_READING_FINISHED, {
        'temperature': temperature,
        'humidity': humidity,
        'sound': sound,
        'datetime': datetime.now()
      }))

      self.e.wait(self.reading_delay)
      if not self.running:
        break

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
