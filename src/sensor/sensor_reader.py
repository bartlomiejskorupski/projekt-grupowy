from random import random
import src.misc.logger as logger
log = logger.getLogger(__name__)

# TODO: Implement get reading methods

class SensorReader:

  def __init__(self):
    pass

  def getTemperatureReading(self) -> float:
    return (random()*5.0)+14

  def getPressureReading(self) -> float:
    return (random()*2.0)+10
