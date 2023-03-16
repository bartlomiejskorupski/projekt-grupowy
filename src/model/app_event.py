from dataclasses import dataclass
from enum import Enum

class AppEventType(Enum):
  SENSOR_READING_STARTED = 'SENSOR_READING_START'
  SENSOR_READING_FINISHED = 'SENSOR_READING_FINISHED'

@dataclass
class AppEvent():
  event_type: AppEventType
  data: dict

