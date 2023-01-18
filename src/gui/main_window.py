from guizero import App
from src.database.local_context import LocalContext
import logger
LOG = logger.getLogger(__name__)

class MainWindow:
  TITLE = 'Projekt Grupowy'
  WIDTH = 1000
  HEIGHT = 1000

  def __init__(self):
    self.app = App(
      title=self.TITLE,
      width=self.WIDTH,
      height=self.HEIGHT,
      layout='grid')

    # init components
    LOG.debug('Initializing components')

    self.db_context = LocalContext()

    LOG.debug('Application started')
    self.app.display()
  
  