from guizero import Box, Text, PushButton, TextBox, error, yesno, info
from src.database.local_context import LocalContext
from env import DEBUG_BORDER
from src.misc.utils import addPadding, getDateString
from datetime import datetime, timedelta
from src.model.reading import ReadingType
from src.database.remote_context import RemoteContext


from src.misc.logger import getLogger
LOG = getLogger(__name__)

class SettingsView:
  '''
  View used for setting datetime intervals for plot view.
  '''

  main_window = None
  db_context: LocalContext
  remote_context: RemoteContext

  container: Box

  button_box: Box
  save_button: PushButton
  reset_button: PushButton
  test_button: PushButton
  export_button: PushButton
  import_button: PushButton

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

  temp_number_text: Text
  humidity_number_text: Text
  sound_number_text: Text

  temp_from_date: datetime
  temp_to_date: datetime
  humidity_from_date: datetime
  humidity_to_date: datetime
  sound_from_date: datetime
  sound_to_date: datetime

  def __init__(self, main_window):
    self.main_window = main_window
    self.db_context = self.main_window.db_context
    self.remote_context = self.main_window.remote_context
    # LOG.debug(f'From: {getDateTimeString(self.DEFAULT_FROM_DATE)} To: {getDateTimeString(self.DEFAULT_TO_DATE)}')

    DEFAULT_FROM_DATE = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=1)
    DEFAULT_TO_DATE = datetime.now().replace(hour=23, minute=59, second=59)

    self.temp_from_date = DEFAULT_FROM_DATE
    self.temp_to_date = DEFAULT_TO_DATE
    self.humidity_from_date = DEFAULT_FROM_DATE
    self.humidity_to_date = DEFAULT_TO_DATE
    self.sound_from_date = DEFAULT_FROM_DATE
    self.sound_to_date = DEFAULT_TO_DATE

    self.container = Box(
      self.main_window.app,
      layout='auto',
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    self.container.bg = '#222222'

    addPadding(self.container, 10)

    RECORDS_NUM_PREFIX = 'Records: '

    # Temperature

    self.temp_box = Box(
      self.container,
      layout='auto',
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    
    temp_header_box = Box(self.temp_box, align='top', width='fill', border=DEBUG_BORDER)
    Text(temp_header_box, align='left', text='Temperature', size=10)
    self.temp_number_text = Text(temp_header_box, align='right', text='0')
    Text(temp_header_box, align='right', text=RECORDS_NUM_PREFIX)

    self.temp_from_box = Box(
      self.temp_box,
      layout='auto',
      align='left',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    Text(self.temp_from_box, align='left', text='From: ')

    self.create_add_sub_button(self.temp_from_box, self.temp_from_day_subtract_button_click, '<')

    self.temp_from_tb = TextBox(
      self.temp_from_box,
      align='left',
      text=f'{getDateString(self.temp_from_date)}',
      enabled=True)
    self.temp_from_tb.text_size = 12

    self.create_add_sub_button(self.temp_from_box, self.temp_from_day_add_button_click, '>')

    self.temp_to_box = Box(
      self.temp_box,
      layout='auto',
      align='left',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    Text(self.temp_to_box, align='left', text='To: ')

    self.create_add_sub_button(self.temp_to_box, self.temp_to_day_subtract_button_click, '<')

    self.temp_to_tb = TextBox(
      self.temp_to_box,
      align='left',
      text=f'{getDateString(self.temp_to_date)}',
      enabled=True)
    self.temp_to_tb.text_size = 12

    self.create_add_sub_button(self.temp_to_box, self.temp_to_day_add_button_click, '>')

    # Humidity

    self.humidity_box = Box(
      self.container,
      layout='auto',
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    
    humidity_header_box = Box(self.humidity_box, align='top', width='fill', border=DEBUG_BORDER)
    Text(humidity_header_box, align='left', text='Humidity', size=10)
    self.humidity_number_text = Text(humidity_header_box, align='right', text='0')
    Text(humidity_header_box, align='right', text=RECORDS_NUM_PREFIX)
    
    self.humidity_from_box = Box(
      self.humidity_box,
      layout='auto',
      align='left',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    Text(self.humidity_from_box, align='left', text='From: ')

    self.create_add_sub_button(self.humidity_from_box, self.humidity_from_day_subtract_button_click, '<')

    self.humidity_from_tb = TextBox(
      self.humidity_from_box,
      align='left',
      text=f'{getDateString(self.humidity_from_date)}',
      enabled=True)
    self.humidity_from_tb.text_size = 12

    self.create_add_sub_button(self.humidity_from_box, self.humidity_from_day_add_button_click, '>')

    self.humidity_to_box = Box(
      self.humidity_box,
      layout='auto',
      align='left',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    Text(self.humidity_to_box, align='left', text='To: ')

    self.create_add_sub_button(self.humidity_to_box, self.humidity_to_day_subtract_button_click, '<')

    self.humidity_to_tb = TextBox(
      self.humidity_to_box,
      align='left',
      text=f'{getDateString(self.humidity_to_date)}',
      enabled=True)
    self.humidity_to_tb.text_size = 12

    self.create_add_sub_button(self.humidity_to_box, self.humidity_to_day_add_button_click, '>')

    # Sound

    self.sound_box = Box(
      self.container,
      layout='auto',
      align='top',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)
    
    sound_header_box = Box(self.sound_box, align='top', width='fill', border=DEBUG_BORDER)
    Text(sound_header_box, align='left', text='Sound', size=10)
    self.sound_number_text = Text(sound_header_box, align='right', text='0')
    Text(sound_header_box, align='right', text=RECORDS_NUM_PREFIX)

    self.sound_from_box = Box(
      self.sound_box,
      layout='auto',
      align='left',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    Text(self.sound_from_box, align='left', text='From: ')

    self.create_add_sub_button(self.sound_from_box, self.sound_from_day_subtract_button_click, '<')

    self.sound_from_tb = TextBox(
      self.sound_from_box,
      align='left',
      text=f'{getDateString(self.sound_from_date)}',
      enabled=True)
    self.sound_from_tb.text_size = 12

    self.create_add_sub_button(self.sound_from_box, self.sound_from_day_add_button_click, '>')

    self.sound_to_box = Box(
      self.sound_box,
      layout='auto',
      align='left',
      width='fill',
      height='fill',
      border=DEBUG_BORDER)

    Text(self.sound_to_box, align='left', text='To: ')

    self.create_add_sub_button(self.sound_to_box, self.sound_to_day_subtract_button_click, '<')

    self.sound_to_tb = TextBox(
      self.sound_to_box,
      align='left',
      text=f'{getDateString(self.sound_to_date)}',
      enabled=True)
    self.sound_to_tb.text_size = 12

    self.create_add_sub_button(self.sound_to_box, self.sound_to_day_add_button_click, '>')

    # Buttons

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
    
    Box(self.button_box, align='right', height='fill', width=10, border=DEBUG_BORDER)

    self.export_button = PushButton(
      self.button_box,
      align='right',
      text='Export',
      command=self.export_button_click)
    
    Box(self.button_box, align='right', height='fill', width=10, border=DEBUG_BORDER)

    self.import_button = PushButton(
      self.button_box,
      align='right',
      text='Import',
      command=self.import_button_click)

    Box(self.button_box, align='right', height='fill', width=10, border=DEBUG_BORDER)

    self.test_button = PushButton(
      self.button_box,
      align='right',
      text='Test',
      command=self.test_button_click)
    
    # Update record number text
    self.temp_number_text.value = self.db_context.readings_count(ReadingType.TEMPERATURE, self.temp_from_date, self.temp_to_date)
    self.humidity_number_text.value = self.db_context.readings_count(ReadingType.HUMIDITY, self.humidity_from_date, self.humidity_to_date)
    self.sound_number_text.value = self.db_context.readings_count(ReadingType.SOUND, self.sound_from_date, self.sound_to_date)
  
  # Create functions

  def create_add_sub_button(self, container: Box, command, text: str) -> PushButton:
    b = PushButton(
      container,
      align='left',
      command=command,
      text=text
    )
    b.text_size = 12
    b.padding(6, 0)
    return b


  # Onclicks
  # Temperature
  def temp_from_day_add_button_click(self):
    self.temp_from_date = self.temp_from_date + timedelta(days=1)
    self.temp_from_tb.value = getDateString(self.temp_from_date)
    self.temp_number_text.value = self.db_context.readings_count(ReadingType.TEMPERATURE, self.temp_from_date, self.temp_to_date)
  
  def temp_from_day_subtract_button_click(self):
    self.temp_from_date = self.temp_from_date - timedelta(days=1)
    self.temp_from_tb.value = getDateString(self.temp_from_date)
    self.temp_number_text.value = self.db_context.readings_count(ReadingType.TEMPERATURE, self.temp_from_date, self.temp_to_date)

  def temp_to_day_add_button_click(self):
    self.temp_to_date = self.temp_to_date + timedelta(days=1)
    self.temp_to_tb.value = getDateString(self.temp_to_date)
    self.temp_number_text.value = self.db_context.readings_count(ReadingType.TEMPERATURE, self.temp_from_date, self.temp_to_date)
  
  def temp_to_day_subtract_button_click(self):
    self.temp_to_date = self.temp_to_date - timedelta(days=1)
    self.temp_to_tb.value = getDateString(self.temp_to_date)
    self.temp_number_text.value = self.db_context.readings_count(ReadingType.TEMPERATURE, self.temp_from_date, self.temp_to_date)

  # Humidity
  def humidity_from_day_add_button_click(self):
    self.humidity_from_date = self.humidity_from_date + timedelta(days=1)
    self.humidity_from_tb.value = getDateString(self.humidity_from_date)
    self.humidity_number_text.value = self.db_context.readings_count(ReadingType.HUMIDITY, self.humidity_from_date, self.humidity_to_date)
  
  def humidity_from_day_subtract_button_click(self):
    self.humidity_from_date = self.humidity_from_date - timedelta(days=1)
    self.humidity_from_tb.value = getDateString(self.humidity_from_date)
    self.humidity_number_text.value = self.db_context.readings_count(ReadingType.HUMIDITY, self.humidity_from_date, self.humidity_to_date)

  def humidity_to_day_add_button_click(self):
    self.humidity_to_date = self.humidity_to_date + timedelta(days=1)
    self.humidity_to_tb.value = getDateString(self.humidity_to_date)
    self.humidity_number_text.value = self.db_context.readings_count(ReadingType.HUMIDITY, self.humidity_from_date, self.humidity_to_date)
  
  def humidity_to_day_subtract_button_click(self):
    self.humidity_to_date = self.humidity_to_date - timedelta(days=1)
    self.humidity_to_tb.value = getDateString(self.humidity_to_date)
    self.humidity_number_text.value = self.db_context.readings_count(ReadingType.HUMIDITY, self.humidity_from_date, self.humidity_to_date)

  # Sound
  def sound_from_day_add_button_click(self):
    self.sound_from_date = self.sound_from_date + timedelta(days=1)
    self.sound_from_tb.value = getDateString(self.sound_from_date)
    self.sound_number_text.value = self.db_context.readings_count(ReadingType.SOUND, self.sound_from_date, self.sound_to_date)
  
  def sound_from_day_subtract_button_click(self):
    self.sound_from_date = self.sound_from_date - timedelta(days=1)
    self.sound_from_tb.value = getDateString(self.sound_from_date)
    self.sound_number_text.value = self.db_context.readings_count(ReadingType.SOUND, self.sound_from_date, self.sound_to_date)

  def sound_to_day_add_button_click(self):
    self.sound_to_date = self.sound_to_date + timedelta(days=1)
    self.sound_to_tb.value = getDateString(self.sound_to_date)
    self.sound_number_text.value = self.db_context.readings_count(ReadingType.SOUND, self.sound_from_date, self.sound_to_date)

  
  def sound_to_day_subtract_button_click(self):
    self.sound_to_date = self.sound_to_date - timedelta(days=1)
    self.sound_to_tb.value = getDateString(self.sound_to_date)
    self.sound_number_text.value = self.db_context.readings_count(ReadingType.SOUND, self.sound_from_date, self.sound_to_date)

  # save
  def save_button_click(self):
    if  self.temp_from_date > self.temp_to_date \
    or self.humidity_from_date > self.humidity_to_date \
    or self.sound_from_date > self.sound_to_date:
      error('Error', '"From date" must be less than "To date"')
      return

    self.update_plots()
    info('Success', 'Plots updated')
  
  def update_plots(self):
    self.main_window.plot_view.update_plots(
      self.temp_from_date,
      self.temp_to_date,
      self.humidity_from_date,
      self.humidity_to_date,
      self.sound_from_date,
      self.sound_to_date)

  def reset_button_click(self):
    DEFAULT_FROM_DATE = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=1)
    DEFAULT_TO_DATE = datetime.now().replace(hour=23, minute=59, second=59)

    self.temp_from_date = DEFAULT_FROM_DATE
    self.temp_to_date = DEFAULT_TO_DATE
    self.temp_from_tb.value = getDateString(self.temp_from_date)
    self.temp_to_tb.value = getDateString(self.temp_to_date)
    self.humidity_from_date = DEFAULT_FROM_DATE
    self.humidity_to_date = DEFAULT_TO_DATE
    self.humidity_from_tb.value = getDateString(self.humidity_from_date)
    self.humidity_to_tb.value = getDateString(self.humidity_to_date)
    self.sound_from_date = DEFAULT_FROM_DATE
    self.sound_to_date = DEFAULT_TO_DATE
    self.sound_from_tb.value = getDateString(self.sound_from_date)
    self.sound_to_tb.value = getDateString(self.sound_to_date)

  def test_button_click(self):
    pass

  def export_button_click(self):
    if not yesno('Export', 'Are you sure you want to export local data to the remote database?'):
      return

    readings = self.db_context.fetch_all()
    success = self.remote_context.export_to_remote(readings)

    if success:
      info('Export', 'Local data exported to remote database.')
    else:
      error('Error', 'Error connecting to the database. Check your network connection.')

  def import_button_click(self):
    if not yesno('Import', 'Are you sure you want to import data from the remote database?'):
      return
    
    imported_readings = self.remote_context.import_from_remote()

    if not imported_readings:
      error('Error', 'Error connecting to the database. Check your network connection.')
      return
    
    imported_readings_mapped = {}
    for r in imported_readings:
      imported_readings_mapped[str(r[0])] = r[:]

    old_readings = self.db_context.fetch_all()
    old_readings_mapped = {}
    for r in old_readings:
      old_readings_mapped[str(r[0])] = r[:]

    new_reading_count = 0
    old_reading_count = 0
    changed_reading_count = 0
    for rid in imported_readings_mapped:
      if not rid in old_readings_mapped.keys():
        new_reading_count += 1
      elif old_readings_mapped[rid] == imported_readings_mapped[rid]:
        old_reading_count += 1
      else:
        changed_reading_count += 1
    missing_reading_count = len(old_readings) - old_reading_count - new_reading_count - changed_reading_count
    
    LOG.info(f'''
      Importing successfull:
        Old_reading_count = {old_reading_count}.
        New_reading_count = {new_reading_count}.
        Changed_reading_count = {changed_reading_count}.
        Missing_reading_count = {missing_reading_count}.
    ''')

    if not yesno('Import', f'''
Successfully imported {len(imported_readings)} readings. There are {len(old_readings)} readings in local db. Are you sure you want to overwrite local data?
    '''):
      return

    LOG.info('Overwriting local data.')
    self.db_context.delete_all_readings()
    self.db_context.save_readings(imported_readings)

