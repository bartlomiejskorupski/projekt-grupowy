from dataclasses import dataclass
from datetime import datetime

@dataclass
class Reading:
  date: datetime
  value: float