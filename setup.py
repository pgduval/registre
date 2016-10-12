import os
import getpass

user = getpass.getuser()
# Settings
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
# DIR_PATH = '/home/elmaster/scraper/registre_foncier/'
CHROME_PATH = '/home/{0}/chromedriver'.format(user)
BROWSERMOB_PATH = '/home/{0}/browsermob-proxy-2.1.2/bin/browsermob-proxy'.format(user)

DB_PATH = os.path.join('sqlite:///' + DIR_PATH, 'db', 'data.db')
PATH_OUT = os.path.join(DIR_PATH, 'output')
LOG_PATH = os.path.join(DIR_PATH, 'log')

dict_map_city = {"27043": 'st_joseph_de_beauce'}
CITY = "27043"
MIN_LOTS_SESSION = 35
MAX_LOTS_SESSION = 85
