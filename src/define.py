import os
from pathlib import Path
from xdg import xdg_data_home
from dotenv import load_dotenv

load_dotenv()

APP_ID   = 'xyz.slothlife.diveboard'
RES_PATH = '/xyz/slothlife/diveboard'
API_KEY  = os.getenv('DIVEBOARD_API_KEY')
SERVER_URL = 'https://www.diveboard.com/'
API_URL  = SERVER_URL + 'api/'
VERSION  = '0.1.0'
# /home/<user>/.var/app/xyz.slothlife.diveboard/data/diveboard.sqlite3
DATABASE_FILE = os.path.join(xdg_data_home(), 'diveboard.sqlite3')
DATA_PATH = xdg_data_home()

DIVE_THUMBNAIL_PATH = f'{DATA_PATH}/dive-thumbnails'

