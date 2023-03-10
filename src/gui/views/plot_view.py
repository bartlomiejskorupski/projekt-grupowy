from guizero import Box, Text, PushButton, Picture
from src.database.local_context import LocalContext
from env import DEBUG_BORDER
from src.misc.utils import addPadding
from src.model.reading import ReadingType
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
from PIL import Image
from io import BytesIO


import src.misc.logger as logger
LOG = logger.getLogger(__name__)

class PlotView:
  main_window = None
  db_context: LocalContext
  container: Box
  
  temp_plot_pic: Picture
  humid_plot_pic: Picture
  sound_plot_pic: Picture

  PLOT_WITDH = 430
  PLOT_HEIGHT = 260

  temp_from_date = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=1)
  temp_to_date = datetime.now().replace(hour=23, minute=59, second=59)
  humid_from_date = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=1)
  humid_to_date = datetime.now().replace(hour=23, minute=59, second=59)
  sound_from_date = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=1)
  sound_to_date = datetime.now().replace(hour=23, minute=59, second=59)

  mpl.rcParams['text.color'] = 'white'
  mpl.rcParams['axes.labelcolor'] = 'white'
  mpl.rcParams['xtick.color'] = 'white'
  mpl.rcParams['ytick.color'] = 'white'

  def __init__(self, main_window):
    self.main_window = main_window
    self.db_context = self.main_window.db_context

    self.container = Box(
      self.main_window.app,
      layout='auto',
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    self.container.bg = '#222222'
    
    self.temp_plot_pic = Picture(
      self.container,
      align='top',
      width=self.PLOT_WITDH,
      height=self.PLOT_HEIGHT)
    
    self.humid_plot_pic = Picture(
      self.container,
      align='top',
      width=self.PLOT_WITDH,
      height=self.PLOT_HEIGHT)
    
    self.sound_plot_pic = Picture(
      self.container,
      align='top',
      width=self.PLOT_WITDH,
      height=self.PLOT_HEIGHT)
  
  def change_plot(self, reading_type: ReadingType):
    self.temp_plot_pic.visible = False
    self.humid_plot_pic.visible = False
    self.sound_plot_pic.visible = False
    if reading_type == ReadingType.TEMPERATURE:
      self.temp_plot_pic.visible = True
    if reading_type == ReadingType.HUMIDITY:
      self.humid_plot_pic.visible = True
    if reading_type == ReadingType.SOUND:
      self.sound_plot_pic.visible = True

  def update_plots(self,
        temp_from_date: datetime,
        temp_to_date: datetime,
        humid_from_date: datetime,
        humid_to_date: datetime,
        sound_from_date: datetime,
        sound_to_date: datetime):
    if self.temp_from_date != temp_from_date or self.temp_to_date != temp_to_date:
      self.temp_from_date = temp_from_date
      self.temp_to_date = temp_to_date
      LOG.debug(f'Updating temperature plot')
      self.update_plot(ReadingType.TEMPERATURE)
    if self.humid_from_date != humid_from_date or self.humid_to_date != humid_to_date:
      self.humid_from_date = humid_from_date
      self.humid_to_date = humid_to_date
      LOG.debug(f'Updating humidity plot')
      self.update_plot(ReadingType.HUMIDITY)
    if self.sound_from_date != sound_from_date or self.sound_to_date != sound_to_date:
      self.sound_from_date = sound_from_date
      self.sound_to_date = sound_to_date
      LOG.debug(f'Updating sound plot')
      self.update_plot(ReadingType.SOUND)

  def update_plot(self, reading_type: ReadingType):
    plot_title = ''
    plot_pic: Picture = None
    date_from = None
    date_to = None
    ylabel = ''
    if reading_type == ReadingType.TEMPERATURE:
      plot_title = 'Temperature'
      plot_pic = self.temp_plot_pic
      date_from = self.temp_from_date
      date_to = self.temp_to_date
      ylabel = '[\u00B0C]'
    if reading_type == ReadingType.HUMIDITY:
      plot_title = 'Humidity'
      plot_pic = self.humid_plot_pic
      date_from = self.humid_from_date
      date_to = self.humid_to_date
      ylabel = '[%]'
    if reading_type == ReadingType.SOUND:
      plot_title = 'Sound'
      plot_pic = self.sound_plot_pic
      date_from = self.sound_from_date
      date_to = self.sound_to_date
      ylabel = '[dB]'

    readings = self.db_context.fetch_readings(reading_type, date_from, date_to)

    dates = []
    values = []
    if len(readings) > 0:
      (_, date_strings, values, _) = list(zip(*readings))
      dates = [datetime.strptime(date_str, self.db_context.DATETIME_FORMAT) for date_str in date_strings]
    mpl.rcParams['text.color'] = 'white'
    mpl.rcParams['axes.labelcolor'] = 'white'
    mpl.rcParams['xtick.color'] = 'white'
    mpl.rcParams['ytick.color'] = 'white'
    fig = plt.figure(facecolor='#222222')
    ax = plt.axes()
    ax.plot(dates, values, 'g-', dates, values, 'r.')

    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    # plt.plot(dates, values, 'g-')
    # plt.plot(dates, values, 'r.')
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.title(plot_title)
    plt.grid(linestyle='--')

    #plt.axis([dates[0], dates[-1], 20, max(values) + 1.0])
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png')
    plt.close()
    image = Image.open(image_buffer)
    plot_pic.image = image
    image_buffer.close()
    LOG.debug(f'{plot_title} plot updated')


