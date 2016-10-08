import random
import csv
import time
import json

import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_random_int(min, max):
    return random.random() * (max - min + 1) + min


def write_list_to_csv(file, data):
    with open(file, "a") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def goto_research(driver, city):
    driver.get("http://www.goazimut.com/GOnet6/index.html?{0}".format(city))

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "dijit_form_Button_0_label")))

    time.sleep(get_random_int(1, 3))
    driver.find_element_by_id("dijit_form_Button_0_label").click()
    time.sleep(get_random_int(1, 3))
    driver.find_element_by_css_selector("div.tab.search").click()
    time.sleep(get_random_int(1, 3))
    return driver


def get_content(log, key_to_find):
    for val in log['entries']:
        if val.get('response'):
            if val['response'].get('content'):
                if val['response']['content'].get('text'):
                    content = json.loads(val['response']['content']['text'])
                    if content.get(key_to_find):
                        return content
    return None


def make_research(proxy, driver, search_term, key_to_find):

    proxy.new_har("log-info", options={'captureHeaders': True,
                                       'captureContent': True})

    driver.find_element_by_id("motCle").clear()
    time.sleep(get_random_int(1, 2))
    driver.find_element_by_id("motCle").send_keys(search_term)
    time.sleep(get_random_int(2, 4))
    driver.find_element_by_id("motCle").send_keys(Keys.ENTER)

    while True:
        if get_content(log=proxy.har['log'], key_to_find=key_to_find):
            return proxy.har['log']
        else:
            time.sleep(10)
