import csv
import time
import platform

from selenium import webdriver

START_TIME = time.time()


# os specific phantom file
if platform.system() == 'Windows':
    PHANTOMJS_PATH = './phantomjs.exe'
else:
    PHANTOMJS_PATH = r'./phantomjs'

INPUT_FILE = '../data/prod_titles.csv'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="|")
    press_source_urls = list(reader)
    press_source_urls.pop(0)


for webpage in press_source_urls:

    site = webpage[0]

    browser = webdriver.PhantomJS(PHANTOMJS_PATH)

    # timeout is 10 minutes
    browser.set_page_load_timeout(60)

    try:

        browser.get(site)

        print(browser.page_source)

    except:

        # timeout
        print("FAILED TO OPEN (timeout): " + site)

    browser.quit()


print("Runtime: " + str(time.time() - START_TIME) + " seconds")