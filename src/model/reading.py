from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class ReadingType(Enum):
  TEMPERATURE = 'temperature'
  HUMIDITY = 'humidity'
  SOUND = 'sound'

@dataclass
class Reading:
  date: datetime
  value: float
  type: str
