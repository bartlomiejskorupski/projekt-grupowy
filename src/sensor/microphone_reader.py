from threading import Thread, Event
from datetime import datetime, timedelta
from queue import Queue, Empty
from src.model.app_event import AppEvent, AppEventType
import env
import sounddevice as sd
import numpy as np
from math import log10

from src.misc.logger import getLogger
LOG = getLogger(__name__)

class MicrophoneReader(Thread):
  ''' Microphone reading thread '''

  event_queue: Queue[AppEvent]

  running: bool
  resume_event: Event

  spq: Queue

  reading_delay: float
  ''' in seconds '''
  sample_delay: float
  ''' in seconds '''

  THRESHOLD = env.SOUND_THRESHOLD
  ''' If this sound threshold is crossed then big reading happens '''

  small_reading_batch: list[float]
  big_reading_beginning_time: datetime

  cooldown_start: datetime
  COOLDOWN = 3.0
  cooldown_activated: bool
  ''' threshold cross cooldown '''

  def __init__(self, event_queue: Queue, reading_delay: int):
    Thread.__init__(self)
    self.daemon = True
    self.running = True
    self.resume_event = Event()
    self.event_queue = event_queue
    self.spq = Queue()
    
    # self.reading_delay = reading_delay/1000.0
    self.reading_delay = env.MICROPHONE_READING_DELAY/1000.0
    self.sample_delay = 0.2

    self.small_reading_batch = []
    self.big_reading_beginning_time = datetime.now()
    self.clear_cooldown()

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
        try:
          self.resume_event.wait(self.sample_delay)
          if not self.running:
            break

          small_reading = self.get_small_reading()
          # print('%.1f' % (small_reading))
          
          # Check if sound threshold was crossed
          threshold_crossed, up, down = False, False, False
          if self.small_reading_batch:
            up, down = self.is_threshold_crossed(self.small_reading_batch[-1], small_reading)
            threshold_crossed = up or down

          do_big_reading = False

          if up and not self.cooldown_activated:
            do_big_reading = True
          elif threshold_crossed:
            # LOG.debug('Activating cooldown.')
            self.activate_cooldown()

          if self.cooldown_went_off():
            # LOG.debug('Cooldown went off.')
            do_big_reading = True
            self.clear_cooldown()
          
          # If the threshold was not crossed then we need to add the last reading to the batch for processing``
          if not threshold_crossed:
            self.small_reading_batch.append(small_reading)

          # Calculate time from beginning of big reading.
          td = datetime.now() - self.big_reading_beginning_time 

          # Begin big reading if 'reading_delay' seconds passed or if small reading threshold was crossed
          if td.total_seconds() >= self.reading_delay or do_big_reading: 
            self.calculate_big_reading()

          # If the threshold was crossed then we need to process the last reading in the next batch
          if threshold_crossed:
            self.small_reading_batch.append(small_reading)
        except Exception as e:
          LOG.error(e)

    LOG.info('Mirophone thread stopped.')
    

  def stop(self):
    LOG.info('Microphone thread stopping...')
    self.running = False
    self.resume_event.set()

  def get_small_reading(self) -> float:
    # Taking sound pressure values from the queue
    max_vals = []
    while True:
      try:
        data = self.spq.get_nowait()
      except Empty:
        break
      # Transforming multiple sound pressure readings into max value from this batch
      abs_data = list(map(lambda val: abs(val), data))
      max_val = max(abs_data)
      max_vals.append(max_val)
    # This gives us sound pressure points [Pa]

    # Calculate effective sound pressure [Pa] from maximum pressure amplitude
    p: float
    try:
      pa = max(max_vals)
      p = pa/1.41421356237
    except:
      p = 0.0
    
    # Calculate decibells with the formula from this site:
    # https://www.engineeringtoolbox.com/sound-pressure-d_711.html
    p_ref = 2e-5
    Lp = 20.0*log10(p/p_ref)
    return Lp

  def calculate_big_reading(self):
    LOG.debug(f'Calculating big reading...')
    big_reading = sum(self.small_reading_batch)/len(self.small_reading_batch)

    # Reading time is set in the middle of the reading begin and end time
    td = datetime.now() - self.big_reading_beginning_time 
    average_reading_time = self.big_reading_beginning_time + td/2

    # Send a reading event to the main thread
    self.event_queue.put(AppEvent(AppEventType.MICROPHONE_BIG_READING, {
      'sound': big_reading,
      'datetime': average_reading_time
    }))

    # Big reading beginning time starts now
    self.big_reading_beginning_time = datetime.now()
    self.small_reading_batch = []

  def is_threshold_crossed(self, prev_reading: float, reading: float) -> tuple[bool, bool]:
    up, down = False, False
    if ( reading >= self.THRESHOLD and prev_reading < self.THRESHOLD ):
      up = True
    if ( reading < self.THRESHOLD and prev_reading >= self.THRESHOLD ):
      down = True
    return (up, down)

  def cooldown_went_off(self):
    td = datetime.now() - self.cooldown_start
    return self.cooldown_activated and td.total_seconds() >= self.COOLDOWN
  
  def activate_cooldown(self):
    self.cooldown_start = datetime.now()
    self.cooldown_activated = True

  def clear_cooldown(self):
    self.cooldown_start = datetime.now()
    self.cooldown_activated = False

  def audio_callback(self, indata, outdata, frames, time, status):
    '''
      Executes roughly once every 0.01s.
      Adds an array of sound pressure values to the sample processing queue.
    '''
    data = indata[::10, 0]
    self.spq.put(data)
    
    

