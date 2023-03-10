from guizero import Box, Text, PushButton, TextBox, error
from src.database.local_context import LocalContext
from env import DEBUG_BORDER
from src.misc.utils import addPadding, getDateString, getDateTimeString
from datetime import datetime, timedelta

import src.misc.logger as logger
LOG = logger.getLogger(__name__)

class SettingsView:
  main_window = None
  db_context: LocalContext

  container: Box

  button_box: Box
  save_button: PushButton
  reset_button: PushButton

  temp_box: Box
  humidity_box: Box
  sound_box: Box

  temp_from_box: Box
  temp_from_tb: TextBox
  temp_to_box: Box
  temp_to_buttons: Box
  temp_to_tb: TextBox

  humidity_from_box: Box
  humidity_from_tb: TextBox
  humidity_to_box: Box
  humidity_to_buttons: Box
  humidity_to_tb: TextBox

  sound_from_box: Box
  sound_from_tb: TextBox
  sound_to_box: Box
  sound_to_buttons: Box
  sound_to_tb: TextBox

  temp_from_date: datetime
  temp_to_date: datetime
  humidity_from_date: datetime
  humidity_to_date: datetime
  sound_from_date: datetime
  sound_to_date: datetime

  DEFAULT_FROM_DATE = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=1)
  DEFAULT_TO_DATE = datetime.now().replace(hour=23, minute=59, second=59)

  def __init__(self, main_window):
    self.main_window = main_window
    self.db_context = self.main_window.db_context
    # LOG.debug(f'From: {getDateTimeString(self.DEFAULT_FROM_DATE)} To: {getDateTimeString(self.DEFAULT_TO_DATE)}')

    self.temp_from_date = self.DEFAULT_FROM_DATE
    self.temp_to_date = self.DEFAULT_TO_DATE
    self.humidity_from_date = self.DEFAULT_FROM_DATE
    self.humidity_to_date = self.DEFAULT_TO_DATE
    self.sound_from_date = self.DEFAULT_FROM_DATE
    self.sound_to_date = self.DEFAULT_TO_DATE

    self.container = Box(
      self.main_window.app,
      layout='auto',
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    self.container.bg = '#222222'

    addPadding(self.container, 10)

    self.temp_box = Box(
      self.container,
      layout='auto',
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    
    temp_header_box = Box(self.temp_box, align='top', width='fill', border=DEBUG_BORDER)
    Text(temp_header_box, align='left', text='Temperature', size=10)
    
    self.humidity_box = Box(
      self.container,
      layout='auto',
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    
    humidity_header_box = Box(self.humidity_box, align='top', width='fill', border=DEBUG_BORDER)
    Text(humidity_header_box, align='left', text='Humidity', size=10)
    
    self.sound_box = Box(
      self.container,
      layout='auto',
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    
    self.button_box = Box(
      self.container,
      align='top',
      width='fill',
      border=DEBUG_BORDER)

    self.save_button = PushButton(
      self.button_box,
      align='right',
      text='Save',
      command=self.save_button_click)
    
    Box(self.button_box, align='right', height='fill', width=10, border=DEBUG_BORDER)

    self.reset_button = PushButton(
      self.button_box,
      align='right',
      text='Reset',
      command=self.reset_button_click)

    sound_header_box = Box(self.sound_box, align='top', width='fill', border=DEBUG_BORDER)
    Text(sound_header_box, align='left', text='Sound', size=10)
    
    # Temperature
    self.temp_from_box = Box(
      self.temp_box,
      layout='auto',
      align='left',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    Text(
      self.temp_from_box,
      align='left',
      text='From: ')

    tfm = PushButton(
      self.temp_from_box,
      align='left',
      command=self.temp_from_day_subtract_button_click,
      text='<')
    tfm.text_size = 12
    tfm.padding(6, 0)

    self.temp_from_tb = TextBox(
      self.temp_from_box,
      align='left',
      text=f'{getDateString(self.temp_from_date)}',
      enabled=False)
    self.temp_from_tb.text_size = 12

    tfp = PushButton(
      self.temp_from_box,
      align='left',
      command=self.temp_from_day_add_button_click,
      text='>'
    )
    tfp.text_size = 12
    tfp.padding(6, 0)

    self.temp_to_box = Box(
      self.temp_box,
      layout='auto',
      align='left',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    Text(
      self.temp_to_box,
      align='left',
      text='To: ')

    ttm = PushButton(
      self.temp_to_box,
      align='left',
      command=self.temp_to_day_subtract_button_click,
      text='<'
    )
    ttm.text_size = 12
    ttm.padding(6, 0)

    self.temp_to_tb = TextBox(
      self.temp_to_box,
      align='left',
      text=f'{getDateString(self.temp_to_date)}',
      enabled=False)
    self.temp_to_tb.text_size = 12

    ttp = PushButton(
      self.temp_to_box,
      align='left',
      command=self.temp_to_day_add_button_click,
      text='>'
    )
    ttp.text_size = 12
    ttp.padding(6, 0)

    # Humidity

    self.humidity_from_box = Box(
      self.humidity_box,
      layout='auto',
      align='left',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    Text(
      self.humidity_from_box,
      align='left',
      text='From: ')

    hfm = PushButton(
      self.humidity_from_box,
      align='left',
      command=self.humidity_from_day_subtract_button_click,
      text='<'
    )
    hfm.text_size = 12
    hfm.padding(6, 0)

    self.humidity_from_tb = TextBox(
      self.humidity_from_box,
      align='left',
      text=f'{getDateString(self.humidity_from_date)}',
      enabled=False)
    self.humidity_from_tb.text_size = 12

    hfp = PushButton(
      self.humidity_from_box,
      align='left',
      command=self.humidity_from_day_add_button_click,
      text='>'
    )
    hfp.text_size = 12
    hfp.padding(6, 0)

    self.humidity_to_box = Box(
      self.humidity_box,
      layout='auto',
      align='left',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    Text(
      self.humidity_to_box,
      align='left',
      text='To: ')

    htm = PushButton(
      self.humidity_to_box,
      align='left',
      command=self.humidity_to_day_subtract_button_click,
      text='<'
    )
    htm.text_size = 12
    htm.padding(6, 0)

    self.humidity_to_tb = TextBox(
      self.humidity_to_box,
      align='left',
      text=f'{getDateString(self.humidity_to_date)}',
      enabled=False)
    self.humidity_to_tb.text_size = 12

    htp = PushButton(
      self.humidity_to_box,
      align='left',
      command=self.humidity_to_day_add_button_click,
      text='>'
    )
    htp.text_size = 12
    htp.padding(6, 0)

    # Sound

    self.sound_from_box = Box(
      self.sound_box,
      layout='auto',
      align='left',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    Text(
      self.sound_from_box,
      align='left',
      text='From: ')

    sfm = PushButton(
      self.sound_from_box,
      align='left',
      command=self.sound_from_day_subtract_button_click,
      text='<'
    )
    sfm.text_size = 12
    sfm.padding(6, 0)

    self.sound_from_tb = TextBox(
      self.sound_from_box,
      align='left',
      text=f'{getDateString(self.sound_from_date)}',
      enabled=False)
    self.sound_from_tb.text_size = 12

    sfp = PushButton(
      self.sound_from_box,
      align='left',
      command=self.sound_from_day_add_button_click,
      text='>'
    )
    sfp.text_size = 12
    sfp.padding(6, 0)

    self.sound_to_box = Box(
      self.sound_box,
      layout='auto',
      align='left',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    Text(
      self.sound_to_box,
      align='left',
      text='To: ')

    stm = PushButton(
      self.sound_to_box,
      align='left',
      command=self.sound_to_day_subtract_button_click,
      text='<'
    )
    stm.text_size = 12
    stm.padding(6, 0)

    self.sound_to_tb = TextBox(
      self.sound_to_box,
      align='left',
      text=f'{getDateString(self.sound_to_date)}',
      enabled=False)
    self.sound_to_tb.text_size = 12

    stp = PushButton(
      self.sound_to_box,
      align='left',
      command=self.sound_to_day_add_button_click,
      text='>'
    )
    stp.text_size = 12
    stp.padding(6, 0)

  # Temperature

  def temp_from_day_add_button_click(self):
    self.temp_from_date = self.temp_from_date + timedelta(days=1)
    self.temp_from_tb.value = getDateString(self.temp_from_date)
  
  def temp_from_day_subtract_button_click(self):
    self.temp_from_date = self.temp_from_date - timedelta(days=1)
    self.temp_from_tb.value = getDateString(self.temp_from_date)

  def temp_to_day_add_button_click(self):
    self.temp_to_date = self.temp_to_date + timedelta(days=1)
    self.temp_to_tb.value = getDateString(self.temp_to_date)
  
  def temp_to_day_subtract_button_click(self):
    self.temp_to_date = self.temp_to_date - timedelta(days=1)
    self.temp_to_tb.value = getDateString(self.temp_to_date)

  # Humidity

  def humidity_from_day_add_button_click(self):
    self.humidity_from_date = self.humidity_from_date + timedelta(days=1)
    self.humidity_from_tb.value = getDateString(self.humidity_from_date)
  
  def humidity_from_day_subtract_button_click(self):
    self.humidity_from_date = self.humidity_from_date - timedelta(days=1)
    self.humidity_from_tb.value = getDateString(self.humidity_from_date)

  def humidity_to_day_add_button_click(self):
    self.humidity_to_date = self.humidity_to_date + timedelta(days=1)
    self.humidity_to_tb.value = getDateString(self.humidity_to_date)
  
  def humidity_to_day_subtract_button_click(self):
    self.humidity_to_date = self.humidity_to_date - timedelta(days=1)
    self.humidity_to_tb.value = getDateString(self.humidity_to_date)

  # Sound

  def sound_from_day_add_button_click(self):
    self.sound_from_date = self.sound_from_date + timedelta(days=1)
    self.sound_from_tb.value = getDateString(self.sound_from_date)
  
  def sound_from_day_subtract_button_click(self):
    self.sound_from_date = self.sound_from_date - timedelta(days=1)
    self.sound_from_tb.value = getDateString(self.sound_from_date)

  def sound_to_day_add_button_click(self):
    self.sound_to_date = self.sound_to_date + timedelta(days=1)
    self.sound_to_tb.value = getDateString(self.sound_to_date)
  
  def sound_to_day_subtract_button_click(self):
    self.sound_to_date = self.sound_to_date - timedelta(days=1)
    self.sound_to_tb.value = getDateString(self.sound_to_date)

  # save button

  def save_button_click(self):
    if  self.temp_from_date > self.temp_to_date \
    or self.humidity_from_date > self.humidity_to_date \
    or self.sound_from_date > self.sound_to_date:
      error('Error', '"From date" must be less than "To date"')
      return

    self.main_window.plot_view.update_plots(
      self.temp_from_date,
      self.temp_to_date,
      self.humidity_from_date,
      self.humidity_to_date,
      self.sound_from_date,
      self.sound_to_date)
  
  def reset_button_click(self):
    self.temp_from_date = self.DEFAULT_FROM_DATE
    self.temp_to_date = self.DEFAULT_TO_DATE
    self.temp_from_tb.value = getDateString(self.temp_from_date)
    self.temp_to_tb.value = getDateString(self.temp_to_date)
    self.humidity_from_date = self.DEFAULT_FROM_DATE
    self.humidity_to_date = self.DEFAULT_TO_DATE
    self.humidity_from_tb.value = getDateString(self.humidity_from_date)
    self.humidity_to_tb.value = getDateString(self.humidity_to_date)
    self.sound_from_date = self.DEFAULT_FROM_DATE
    self.sound_to_date = self.DEFAULT_TO_DATE
    self.sound_from_tb.value = getDateString(self.sound_from_date)
    self.sound_to_tb.value = getDateString(self.sound_to_date)

