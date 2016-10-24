from scrape import *
from setup import *

from browsermobproxy import Server
from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
import time


# Set the proxy
server = Server(BROWSERMOB_PATH)
server.start(options={'log_path': LOG_PATH, 'log_file': 'server.log'})
proxy = server.create_proxy()

# Set the browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
driver = webdriver.Chrome(CHROME_PATH, chrome_options=chrome_options)
driver.set_window_size(1280, 1024)

# Main function
list_lots = []
driver = goto_research(driver, city=CITY)
for i in range(10):
    print("Enum with term set to {0}".format(i))
    log = make_research(proxy,
                        driver,
                        search_term=str(i),
                        key_to_find='adresse')
    content = get_content(log=log, key_to_find='adresse')

    # Extract lot matricule from response
    for adress in content['adresse']:
        list_lots.append(adress['fMat'].replace("-", ""))

    time.sleep(get_random_int(2, 4))

# Remove duplicate and store data
out_lots = [[x] for x in set(list_lots)]
print(len(set(list_lots)), len(list_lots))

write_list_to_csv(os.path.join(PATH_OUT, dict_map_city[CITY] + '.txt'), out_lots)

server.stop()
driver.quit()

# END #
