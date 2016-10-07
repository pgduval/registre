from browsermobproxy import Server

from selenium import webdriver

# Set the proxy
server = Server(BROWSERMOB_PATH)
server.start(options={'log_path': PATH_OUT, 'log_file': 'server.log'})
proxy = server.create_proxy()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
driver = webdriver.Chrome(CHROME_PATH, chrome_options=chrome_options)

# Load list of lots
with open(os.path.join(PATH_OUT, dict_map_city[CITY] + '.txt')) as f:
    all_lots = f.readlines()

print(all_lots)
# Main function
driver = goto_research(driver, city=CITY)
for lot in all_lots[0]:
    # Search
lot = '7529865546'
result = make_research(proxy,
                       driver,
                       search_term=lot,
                       key_to_find='infoLots')
# Extract content
content = get_content(result, key_to_find='infoLots')

print(content.keys())

for key, val in content.items():
    print(key)
    if isinstance(val, dict):
        print("-------")
        print(key, val.keys())

'', 
'', 
'', 
'', 
'', 
'', 
'',
''

print(content['croquis'])
print(content['infoLots'])
print(content['zonage'])
print(content['photos'])
print(content['proprietaires'])
print(content['valeurRole'])
print(content['adresses'])
print(content['infoGenerale'])



print(content['proprietaires'])
# Wait
time.sleep(get_random_int(2, 4))

server.stop()
driver.quit()




print(proxy.har['log'])
log = proxy.har['log']

for val in log['entries']:
    if val.get('response'):
        if val['response'].get('content'):
            if val['response']['content'].get('text'):
                content = json.loads(val['response']['content']['text'])
                print("-----------------------")
                # print(content)
                if content.get('infoLots'):
                    print(content)



test = get_content(log, key_to_find='infoLots')
print(test.keys())
test = get_content(log, key_to_find='infoGenerale')
print(test)
for val in test:
    print(val)

print(test)
for i in range(10):
    print("Enum with term set to {0}".format(i))
    content = make_research(driver,
                            search_term=str(i),
                            key_to_find='adresse')

    # Extract lot matricule from response
    for adress in content:
        list_lots.append(adress['fMat'].replace("-", ""))

    time.sleep(get_random_int(2, 4))




# END #
