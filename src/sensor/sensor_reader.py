from random import random
import src.misc.logger as logger
LOG = logger.getLogger(__name__)

try:
  import Adafruit_DHT as DHT
except ModuleNotFoundError as e:
  LOG.warning('Adafruit_DHT module not found! Using fake one.')
  import src.misc.fake_dht as DHT


# TODO: Implement get reading methods

class SensorReader:

  def __init__(self):
    self.sensor = DHT.DHT22
    self.pin = 4

  def getHumidityAndTemperatureReading(self) -> tuple[float, float]:
    LOG.debug('Begin temperature and humidity reading.')
    _, temp = DHT.read_retry(self.sensor,self.pin)
    LOG.debug(f'Temperature reading: {temp:.2f}')
    return (0.0, temp)

  def getSoundReading(self) -> float:
    return 0.0
