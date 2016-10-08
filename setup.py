import os

# Settings
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join('sqlite:///' + DIR_PATH, 'db', 'data.db')

CHROME_PATH = '/home/elmaster/chromedriver'
BROWSERMOB_PATH = '/home/elmaster/browsermob-proxy-2.1.2/bin/browsermob-proxy'
dict_map_city = {"27043": 'st_joseph_de_beauce'}
CITY = "27043"
PATH_OUT = os.path.join(DIR_PATH, 'output')
