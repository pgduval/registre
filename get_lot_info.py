from scrape import *
from setup import *

from browsermobproxy import Server
from selenium import webdriver

import os
import time
import logging


def json_to_csv(data, file):
    json.dump(data, open(os.path.join(PATH_OUT, 'raw', file + '.txt'), 'w'))


def get_job():

    # Load list of lots
    with open(os.path.join(PATH_OUT, dict_map_city[CITY] + '.txt')) as f:
        all_lots_tmp1 = f.readlines()

    # Insure unique and strip "\n" character
    all_lots_tmp2 = list(set([x.rstrip() for x in all_lots_tmp1]))

    # Remove lots already extracted
    list_scraped = [x.strip(".txt") for x in os.listdir(os.path.join(PATH_OUT, 'raw'))]
    all_lots_tmp3 = [x for x in all_lots_tmp2 if x not in list_scraped]

    return all_lots_tmp3


# Set logging
logging.basicConfig(filename=os.path.join(LOG_PATH, 'extract.log'),
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

# Set the proxy
server = Server(BROWSERMOB_PATH)
server.start(options={'log_path': PATH_OUT, 'log_file': 'server.log'})
proxy = server.create_proxy()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
driver = webdriver.Chrome(CHROME_PATH, chrome_options=chrome_options)
driver.set_window_size(1280, 1024)


# Main function
all_lots = get_job()
print("{} jobs remaining".format(len(all_lots)))

logging.info('--- Start extraction session ---')

driver = goto_research(driver, city=CITY)
list_error = []
for idx, lot in enumerate(all_lots[0:30]):

    try:
        print("\nExtracting lot  #{0}".format(lot))
        print("{0} out of {1}".format(idx + 1, len(all_lots)))

        # Search
        result = make_research(proxy, driver,
                               search_term=lot,
                               key_to_find='infoLots')
        # Extract content
        content = get_content(result, key_to_find='infoLots')

        # Write result
        json_to_csv(data=content, file=lot)

        # Wait
        time.sleep(get_random_int(2, 4))
        print("Extraction completed")

    except:
        print("-->Error")
        logging.warning('Failed extraction for lot: {0}'.format(lot))
        list_error.append(lot)

server.stop()
driver.quit()

logging.info('---- Extraction session stats ------')
logging.info('Number of failure: {0}'.format(len(list_error)))
logging.info('List of failure {0}'.format(list_error))
logging.info('---- End extraction session ------')

# END #
