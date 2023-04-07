from datetime import datetime
from queue import Queue
from threading import Thread, Event
from src.model.app_event import AppEvent, AppEventType

from src.misc.logger import getLogger
LOG = getLogger(__name__)

try:
  import Adafruit_DHT as DHT
except ModuleNotFoundError:
  LOG.warning('Adafruit_DHT module not found! Using fake one.')
  import src.misc.fake_dht as DHT

class SensorReader(Thread):
  running: bool
  resume_event: Event
  reading_delay: float

  event_queue: Queue[AppEvent]

  prev_humid_reading: float = None
  prev_temp_reading: float = None
  prev_reading_time: datetime = None

  def __init__(self, event_queue: Queue, reading_delay: int):
    ''' reading_delay - time between readings in milliseconds '''
    Thread.__init__(self)
    self.daemon = True
    self.sensor = DHT.DHT22
    self.pin = 12
    self.running = True
    self.resume_event = Event()
    self.event_queue = event_queue
    self.reading_delay = reading_delay/1000.0

  def run(self):
    LOG.info('Sensor thread started.')
    while True:
      LOG.info('Reading started...')

      self.resume_event.wait(self.reading_delay)
      if not self.running:
        break

      self.event_queue.put(AppEvent(AppEventType.SENSOR_READING_STARTED, {}))

      # read_retry takes anywhere from 0 to 30 seconds to complete
      humidity, temperature = DHT.read_retry(self.sensor, self.pin)
      
      reading_valid = self.is_valid_reading(humidity, temperature)

      dt_now = datetime.now()
      self.prev_humid_reading = humidity
      self.prev_temp_reading = temperature
      self.prev_reading_time = dt_now

      if not reading_valid:
        LOG.error('Reading finished with an error. Retrying...')
        continue

      LOG.info('Reading finished.')
      self.event_queue.put(AppEvent(AppEventType.SENSOR_READING_FINISHED, {
        'temperature': temperature,
        'humidity': humidity,
        'datetime': dt_now
      }))
        
    LOG.info('Sensor thread stopped.')

  def stop(self):
    LOG.info('Sensor thread stopping...')
    self.running = False
    self.resume_event.set()

  def is_valid_reading(self, humidity: float, temperature: float) -> bool:
    # Check if reading failed
    if not humidity or not temperature:
      LOG.error('Reading is null')
      return False

    # Check humidity
    if not 0.0 <= humidity <= 100.0:
      LOG.error(f'Invalid humidity value: {humidity}')
      return False
    
    # Check for changes that are too big compared to previous measurements

    # Ignore first readings
    if not self.prev_humid_reading or not self.prev_temp_reading or not self.prev_reading_time:
      return True
    
    # Max change per reading
    MAX_HUMID_CHANGE = 10.0
    MAX_TEMP_CHANGE = 5.0

    dt_now = datetime.now()
    dt = dt_now - self.prev_reading_time
    passed_seconds = dt.total_seconds()

    humid_change = abs(humidity - self.prev_humid_reading)
    temp_change = abs(temperature - self.prev_temp_reading)

    LOG.debug(f'''
        Reading = ({humidity}, {temperature}).
        Previous reading = ({self.prev_humid_reading}, {self.prev_temp_reading})
        Seconds passed = {passed_seconds}s
        Change = ({humid_change}, {temp_change})
        Max change = ({MAX_HUMID_CHANGE}, {MAX_TEMP_CHANGE})
      ''')

    if humid_change > MAX_HUMID_CHANGE or temp_change > MAX_TEMP_CHANGE:
      LOG.error('Reading change is too high.')
      return False
    
    return True
