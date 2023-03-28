from threading import Thread, Event
from datetime import datetime
from queue import Queue, Empty
from src.model.app_event import AppEvent, AppEventType
import sounddevice as sd
import numpy as np

from src.misc.logger import getLogger
LOG = getLogger(__name__)

class MicrophoneReader(Thread):
  ''' Microphone reading thread '''

  event_queue: Queue[AppEvent]

  running: bool
  resume_event: Event

  spq: Queue
  
  def __init__(self, event_queue: Queue, reading_delay: int):
    Thread.__init__(self)
    self.daemon = True
    self.running = True
    self.resume_event = Event()
    self.event_queue = event_queue
    self.spq = Queue()
    
    
    # self.reading_delay = reading_delay/1000.0
    self.reading_delay = 1.0

  def run(self):
    LOG.info('Microphone thread started.')

    device_info = sd.query_devices('default', 'input')
    samplerate = device_info['default_samplerate']

    stream = sd.Stream(
      channels=1,
      samplerate=samplerate,
      callback=self.audio_callback)
    with stream:
      while True:

        # Taking sound pressure values from the queue
        max_vals = []
        while True:
          # Transforming multiple sound pressure readings into max value from this batch
          try:
            data = self.spq.get_nowait()
          except Empty:
            break
          abs_data = list(map(lambda val: abs(val), data))
          max_val = max(abs_data)
          max_vals.append(max_val)
        if max_vals:
          avg_val = sum(max_vals)/len(max_vals)
          print(f'{avg_val:.2f}')

        self.resume_event.wait(self.reading_delay)
        if not self.running:
          break

  def stop(self):
    LOG.info('Microphone thread stopping...')
    self.running = False
    self.resume_event.set()

  def audio_callback(self, indata, outdata, frames, time, status):
    data = indata[::10, 0]
    self.spq.put(data)
    
    

