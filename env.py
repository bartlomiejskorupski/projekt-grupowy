import sys

APP_VERSION = '1.2'
APP_NAME = 'SensorManager'
DATA_FOLDER_PATH = '/var/lib/sensormanager'

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 320

DEBUG_BORDER = '--debug-border' in sys.argv
FULL_SCREEN = '--full-screen' in sys.argv

PROJECT_PATH = ''
for arg in sys.argv:
    if arg.startswith('--project-path='):
        PROJECT_PATH = arg[15:]
