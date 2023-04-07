from threading import Thread, Event
from datetime import datetime
from queue import Queue, Empty
from src.model.app_event import AppEvent, AppEventType
import env
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

  reading_delay: float
  ''' in seconds '''
  sample_delay: float
  ''' in seconds '''

  THRESHOLD = env.SOUND_THRESHOLD
  ''' If this sound threshold is crossed then big reading happens '''
  
  def __init__(self, event_queue: Queue, reading_delay: int):
    Thread.__init__(self)
    self.daemon = True
    self.running = True
    self.resume_event = Event()
    self.event_queue = event_queue
    self.spq = Queue()
    
    self.reading_delay = reading_delay/1000.0
    self.sample_delay = 0.25

  def run(self):
    LOG.info('Microphone thread started.')

    device_info = sd.query_devices('default', 'input')
    samplerate = device_info['default_samplerate']

    small_reading_batch: list[float] = []
    big_reading_beginning_time = datetime.now()

    stream = sd.Stream(
      channels=1,
      samplerate=samplerate,
      callback=self.audio_callback)
    with stream:
      while True:

        self.resume_event.wait(self.sample_delay)
        if not self.running:
          break

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
        # This gives us discrete sound pressure points

        # We take the max value from these discrete pressure points every 'sample_dalay' seconds
        # and add them to the small_reading_batch
        small_reading = max(max_vals)
        print(small_reading)
        
        # Check if sound threshold was crossed
        threshold_crossed = False
        if len(small_reading_batch) >= 1:
          if ( small_reading >= self.THRESHOLD and small_reading_batch[-1] < self.THRESHOLD ) \
                or \
              ( small_reading < self.THRESHOLD and small_reading_batch[-1] >= self.THRESHOLD ):
            threshold_crossed = True
        
        # If the threshold was not crossed then the big reading time has passed
        # so we need to add the last reading to the batch for processing
        if not threshold_crossed:
          small_reading_batch.append(small_reading)

        # Calculate time from beginning of big reading.
        td = datetime.now() - big_reading_beginning_time
        # Begin big reading if 'self.reading_delay' seconds passed or if small reading threshold was crossed
        if td.total_seconds() >= self.reading_delay or threshold_crossed: 
          LOG.debug(f'Calculating big reading...')
          LOG.debug(small_reading_batch)
          # Big reading is an average value of small readings
          big_reading = sum(small_reading_batch)/len(small_reading_batch)
          # Reading time is set in the middle of the reading begin and end time
          average_reading_time = big_reading_beginning_time + td/2
          # Send a reading event to the main thread
          self.event_queue.put(AppEvent(AppEventType.MICROPHONE_BIG_READING, {
            'sound': big_reading,
            'datetime': average_reading_time
          }))
          # Big reading beginning time starts now
          big_reading_beginning_time = datetime.now()
          # Reset small reading batch
          small_reading_batch = []

        # If the threshold was crossed then we need to process the last reading in the next batch
        if threshold_crossed:
          small_reading_batch.append(small_reading)

    LOG.info('Mirophone thread stopped.')
    

  def stop(self):
    LOG.info('Microphone thread stopping...')
    self.running = False
    self.resume_event.set()

  def audio_callback(self, indata, outdata, frames, time, status):
    '''
      Executes roughly once every 0.01s.
      Adds an array of sound pressure values to the sample processing queue.
    '''
    data = indata[::10, 0]
    self.spq.put(data)
    
    

