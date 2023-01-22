from queue import Queue, Empty
from guizero import App, Box, Text, PushButton
import env
from src.model.app_event import AppEvent, AppEventType
from src.model.reading import Reading
from src.sensor.sensor_reader import SensorReader
from src.gui.views.home_view import HomeView
from src.gui.menu.side_panel import SidePanel
from src.gui.menu.top_panel import TopPanel
from src.database.local_context import LocalContext

import src.misc.logger as logger
LOG = logger.getLogger(__name__)

class MainWindow:
  app: App
  db_context: LocalContext
  
  top_panel: TopPanel
  side_panel: SidePanel
  home_view: HomeView

  READING_DELAY = 5
  sensor_thread: SensorReader
  QUEUE_PROCESSING_DELAY = 100
  event_queue: Queue[AppEvent]

  def __init__(self):
    self.app = App(
      title=env.APP_NAME,
      width=env.WINDOW_WIDTH,
      height=env.WINDOW_HEIGHT,
      layout='auto')
    self.app.font = 'Ubuntu'
    self.app.text_color = 'white'
    self.app.when_key_pressed = self.key_pressed
    self.app.when_closed = self.close_app
    if env.FULL_SCREEN:
      self.app.set_full_screen()

    self.db_context = LocalContext()
    self.event_queue = Queue()
    self.app.after(time=self.QUEUE_PROCESSING_DELAY, function=self.process_queue)

    # init components
    LOG.debug('Initializing components')
    self.top_panel = TopPanel(self.app)
    Box(self.app,layout='auto',align='top',height=0,width='fill',border=True)
    self.side_panel = SidePanel(self)
    Box(self.app,layout='auto',align='left',height='fill',width=0,border=True)
    self.home_view = HomeView(self)

    self.sensor_thread = SensorReader(self.event_queue, self.READING_DELAY)
    self.sensor_thread.start()

    self.app.display()
  
  def process_queue(self):
    while self.event_queue.qsize():
      try:
        e = self.event_queue.get(block=False)
        if e.event_type == AppEventType.SENSOR_READING_STARTED:
          pass
        elif e.event_type == AppEventType.SENSOR_READING_FINISHED:
          LOG.debug(f'Temp: {e.data["temperature"]}')
          self.db_context.save_reading(Reading(e.data['datetime'], e.data['temperature']))
          self.home_view.update_reading_texts(e.data['temperature'], e.data['humidity'], e.data['sound'])
      except Empty:
        LOG.debug('Queue is empty.')
    self.app.after(time=self.QUEUE_PROCESSING_DELAY, function=self.process_queue)
    
  def key_pressed(self, event):
    if event.key == '\u001B':
      pass
  
  def close_app(self):
    self.sensor_thread.stop()
    LOG.debug('App closing')
    self.app.destroy()

