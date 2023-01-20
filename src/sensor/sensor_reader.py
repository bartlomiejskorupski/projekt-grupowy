import Adafruit_DHT as dht
from random import random
import src.misc.logger as logger
log = logger.getLogger(__name__)

# TODO: Implement get reading methods

class SensorReader:

  def __init__(self):
    self.sensor = dht.DHT22
    self.pin = 4

  def getTemperatureReading(self) -> float:
    _,temp = dht.read_retry(self.sensor,self.pin)
    log.debug(f'temperatur reading, {temp}')
    return temp

  def getPressureReading(self) -> float:
    return 0.0

  def getSoundReading(self) -> float:
    return 0.0
