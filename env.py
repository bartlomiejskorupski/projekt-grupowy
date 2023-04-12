import sys

APP_VERSION = '1.3'
APP_NAME = 'SensorManager'
DATA_FOLDER_PATH = '/var/lib/sensormanager'
REMOTE_DATABASE_URL = 'https://sensormanager-9de90-default-rtdb.europe-west1.firebasedatabase.app/'

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 320

DEBUG_BORDER = '--debug-border' in sys.argv
FULL_SCREEN = '--full-screen' in sys.argv
PRODUCTION = '--prod' in sys.argv


PROJECT_PATH = ''
FIREBASE_CERTIFICATE_PATH = ''
SOUND_THRESHOLD = 60.0
READING_DELAY = 60_000
for arg in sys.argv:
    if arg.startswith('--project-path='):
        PROJECT_PATH = arg[15:]
    if arg.startswith('--firebase-cert-path='):
        FIREBASE_CERTIFICATE_PATH = arg[21:]
    if arg.startswith('--sound-threshold='):
        SOUND_THRESHOLD = float(arg[18:])
    if arg.startswith('--reading-delay='):
        READING_DELAY = float(arg[16:])

