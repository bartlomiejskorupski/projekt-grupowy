import firebase_admin as fba
from firebase_admin import db, credentials
from env import REMOTE_DATABASE_URL, FIREBASE_CERTIFICATE_PATH, PRODUCTION
import json

from src.misc.logger import getLogger
LOG = getLogger(__name__)

class RemoteContext:
  ''' Firebase remote database connection object. '''

  fb_app: fba.App
  ''' Firebase application. None if certificate wasn't loaded. '''

  def __init__(self):
    try:
      cred = credentials.Certificate(FIREBASE_CERTIFICATE_PATH)
      LOG.info('Firebase certificate loaded successfully')
      self.fb_app = fba.initialize_app(cred, {
        'databaseURL': REMOTE_DATABASE_URL,
        'httpTimeout': 5
      })
      LOG.info('Firebase app initialized')
    except:
      self.fb_app = None
      LOG.error('Error loading firebase certificate. File not found or its contents are invalid.')
    

  def export_to_remote(self, readings: list[tuple]) -> bool:
    '''
    Export local data to remote database server.
    This action erases data from the remote database and replaces it with local data.

    Args:
      readings: List of tuples in a format: (id: int, date_str: str, value: float, type: str)
    
    Returns:
      True if export was successfull or False if an error occurs during communication with remote database
    '''

    # if not PRODUCTION:
    #   return False

    if not self.fb_app:
      return False

    ref = db.reference('/')

    mapped_readings = list(map(lambda r: {'id': r[0], 'date': r[1], 'value': r[2], 'type': r[3]}, readings))
    exported_dict = {
      'readings': mapped_readings
    }

    try:
      ref.set(exported_dict)
      LOG.debug('Firebase database overwritten')
    except:
      LOG.error('Database connection error')
      return False
    return True


  def import_from_remote(self) -> list[tuple]:
    '''
    Import data from remote database.

    Returns:
      readings: List of tuples in a format: (id: int, date_str: str, value: float, type: str)
    '''

    if not self.fb_app:
      return False

    ref = db.reference('/readings')

    try:
      readings = ref.get()
      mapped_readings = list(map(lambda r: (r['id'], r['date'], r['value'], r['type']), readings))
      LOG.debug('Remote data imported successfully')
      return mapped_readings
    except:
      LOG.error('Database connection error')
      return []
      
