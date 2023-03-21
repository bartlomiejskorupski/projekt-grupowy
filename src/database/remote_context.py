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

    exported_dict = {
      "readings": {}
    }
    
    for r in readings:
      uid, date_str, value, rtype = r
      exported_dict['readings'][str(uid)] = {
        'date': date_str,
        'value': value,
        'type': rtype
      }

    success = True
    try:
      ref.set(exported_dict)
      LOG.debug('Firebase database overwritten')
    except:
      LOG.error('Database connection error')
      success = False
    return success


