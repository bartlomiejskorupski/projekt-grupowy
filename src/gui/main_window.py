from queue import Queue, Empty
from guizero import App, Box
import env
from src.gui.views.settings_view import SettingsView
from src.gui.views.plot_view import PlotView
from src.model.app_event import AppEvent, AppEventType
from src.model.reading import Reading, ReadingType
from src.sensor.sensor_reader import SensorReader
from src.sensor.microphone_reader import MicrophoneReader
from src.gui.views.home_view import HomeView
from src.gui.menu.side_panel import SidePanel
from src.gui.menu.top_panel import TopPanel
from src.database.local_context import LocalContext
from src.database.remote_context import RemoteContext

from src.misc.logger import getLogger
LOG = getLogger(__name__)

class MainWindow:
  '''
  Window containing all elements of the application.
  '''

  app: App
  db_context: LocalContext
  remote_context: RemoteContext
  
  top_panel: TopPanel
  side_panel: SidePanel
  home_view: HomeView
  settings_view: SettingsView
  plot_view: PlotView

  READING_DELAY = env.READING_DELAY
  """ Delay between readings in ms """

  sensor_thread: SensorReader
  microphone_thread: MicrophoneReader
  QUEUE_PROCESSING_DELAY = 100
  event_queue: Queue[AppEvent]
  """ One-way event queue used for communicating with the SensorReader thread """
  

  def __init__(self):
    self.app = App(
      title=env.APP_NAME,
      width=env.WINDOW_WIDTH,
      height=env.WINDOW_HEIGHT,
      layout='auto')
    self.app.font = 'Ubuntu'
    self.app.text_size = 8
    self.app.text_color = 'white'
    self.app.when_closed = self.close_app

    if env.FULL_SCREEN:
      self.app.set_full_screen()

    # Initialize database connection
    self.db_context = LocalContext()
    self.remote_context = RemoteContext()

    # Initialize SensorReader event queue and start the processing method
    self.event_queue = Queue()
    self.app.after(time=self.QUEUE_PROCESSING_DELAY, function=self.process_queue)

    # Initialize components
    LOG.debug('Initializing components')
    self.top_panel = TopPanel(self)
    Box(self.app,layout='auto',align='top',height=0,width='fill',border=True) # Horizontal line
    self.side_panel = SidePanel(self)
    Box(self.app,layout='auto',align='left',height='fill',width=0,border=True) # Vertical line

    self.side_panel.clear_buttons_bg()
    self.side_panel.home_button.bg = self.side_panel.HIGHLIGHTED_COLOR

    # Initialize views
    self.home_view = HomeView(self)
    self.home_view.update_reading_texts(None, None, self.READING_DELAY)
    self.settings_view = SettingsView(self)
    self.plot_view = PlotView(self)

    # Setting home as the default view
    self.home_button_click()

    # Initial plot update
    self.settings_view.update_plots()

    # Initializing and starting the reader threads
    self.sensor_thread = SensorReader(self.event_queue, self.READING_DELAY)
    self.sensor_thread.start()
    self.microphone_thread = MicrophoneReader(self.event_queue, self.READING_DELAY)
    self.microphone_thread.start()

  def open(self):
    self.app.display()
  
  def process_queue(self):
    '''
    This method reads and processes SensorReader thread's messages from the event queue. 
    '''
    while self.event_queue.qsize():
      try:
        e = self.event_queue.get(block=False)
        if e.event_type == AppEventType.SENSOR_READING_STARTED:
          self.home_view.reading_started()
        elif e.event_type == AppEventType.SENSOR_READING_FINISHED:
          temp, humid, date = e.data['temperature'], e.data['humidity'], e.data['datetime']
          if temp is None:
            LOG.warning('Reading failed.')
          else:
            LOG.debug(f'Measured temperature: {temp}')
            self.db_context.save_reading(Reading(date, temp, ReadingType.TEMPERATURE))
            LOG.debug(f'Measured humidity: {humid}')
            self.db_context.save_reading(Reading(date, humid, ReadingType.HUMIDITY))
          self.home_view.update_reading_texts(temp, humid, self.READING_DELAY)
        elif e.event_type == AppEventType.MICROPHONE_BIG_READING:
          sound, date = e.data['sound'], e.data['datetime']
          LOG.debug(f'Sound reading: {sound}')
          self.db_context.save_reading(Reading(date, sound, ReadingType.SOUND))
          self.home_view.update_sound_reading_text(sound)
      except Empty:
        LOG.debug('Queue is empty.')
    # Again start the process_queue method after a delay
    self.app.after(time=self.QUEUE_PROCESSING_DELAY, function=self.process_queue)
  
  def home_button_click(self):
    self.hide_all_views()
    self.home_view.container.visible = True

  def settings_button_click(self):
    self.hide_all_views()
    self.settings_view.container.visible = True

  def temperature_button_click(self):
    self.hide_all_views()
    self.plot_view.change_plot(ReadingType.TEMPERATURE)
    self.plot_view.container.visible = True

  def humidity_button_click(self):
    self.hide_all_views()
    self.plot_view.change_plot(ReadingType.HUMIDITY)
    self.plot_view.container.visible = True

  def sound_button_click(self):
    self.hide_all_views()
    self.plot_view.change_plot(ReadingType.SOUND)
    self.plot_view.container.visible = True

  def home_button_click(self):
    self.hide_all_views()
    self.home_view.container.visible = True

  def hide_all_views(self):
    self.home_view.container.visible = False
    self.settings_view.container.visible = False
    self.plot_view.container.visible = False

  def close_app(self):
    self.sensor_thread.stop()
    self.microphone_thread.stop()
    LOG.debug('App closing')
    self.app.destroy()

