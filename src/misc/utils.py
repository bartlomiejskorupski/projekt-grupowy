from guizero import Box
from datetime import datetime
from env import DEBUG_BORDER

def addPadding(box: Box, padding: int = 10, debug_border: bool = False):
  border = DEBUG_BORDER or debug_border
  Box(box, align='top', width='fill', height=padding, border=border)
  Box(box, align='bottom', width='fill', height=padding, border=border)
  Box(box, align='left', height='fill', width=padding, border=border)
  Box(box, align='right', height='fill', width=padding, border=border)

def getDateString(dt: datetime = None):
  dt = datetime.now() if not dt else dt
  return dt.strftime('%d-%m-%Y')

def getTimeString(dt: datetime = None):
  dt = datetime.now() if not dt else dt
  return dt.strftime('%H:%M')

def getDateTimeString(dt: datetime = None):
  return getDateString(dt) + ' ' + getTimeString(dt)

