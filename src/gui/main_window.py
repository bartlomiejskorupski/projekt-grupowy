from guizero import App
from database.local_context import LocalContext

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

    self.init_db_context()

    self.app.display()

  def init_db_context(self):
    self.db_context = LocalContext()
  