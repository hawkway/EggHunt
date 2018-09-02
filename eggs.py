#!/usr/bin/python

import os
import time
import webbrowser as wb
from datetime import datetime
from selenium import webdriver as driver

#------------------------------------------------------------------------------------
# init vars
last_page = 0
current_page = 0
dPageTargets = {}

# constants
BATCH_SIZE = 20
PATH_CHROMIUM = "/usr/bin/chromium-browser"
CMD_KILL_CHROMIUM = "pkill chromium"
LOG_NAME = datetime.now().strftime("%Y_%m_%d_%H%M%S")
PATH_CHROME_DRIVER = "/usr/lib/chromium-browser/chromedriver"

#------------------------------------------------------------------------------------
# read in data from source files

# get url for site connect
with open('/home/user/projects/eggs/url_login.txt', 'r') as f:
    URL_LOGIN = f.read()

# get url for site browse
with open('/home/user/projects/eggs/url_browse.txt', 'r') as f:
    URL_BROWSE = f.read()

# get url for site browse
with open('/home/user/projects/eggs/url_base_page.txt', 'r') as f:
    URL_BASE_PAGE = f.read()

# get link class name
with open('/home/user/projects/eggs/class_name.txt', 'r') as f:
    TARGET_LINK_CLASS = f.read()

#------------------------------------------------------------------------------------
# simple log function
class Log:
    def __init__(self):
        pass

    def log(self, s):
        # set new name per run
        path = '/home/user/projects/eggs/Log/' + LOG_NAME + '.txt'
        # write contents to disk
        with open(path, 'a') as f:
            f.write(s + '\n')
#------------------------------------------------------------------------------------
# get links to next pages

def get_last_page_num():
    global last_page
    # get all page elements
    pages = browser.find_elements_by_class_name("altlink")

    # get the highest page link
    last_page_link = pages[-2]
    # get href from object
    last_page_url = last_page_link.get_attribute("href")

    # find index of page number
    start_index = last_page_url.find("&page=")
    # get the number of the last page
    last_page = int(last_page_url[start_index+6:])
    # log page number
    log.log("last page: " + str(last_page))
#------------------------------------------------------------------------------------
# get target links from page, and iterate

def get_target_links():
    # return list
    links = []
    # get all target links
    elements = browser.find_elements_by_class_name(TARGET_LINK_CLASS)

    # process links
    for e in elements:
        links.append(e.get_attribute("href"))

    # return all target links
    return links
# ------------------------------------------------------------------------------------
# open target links in browser

def process_targets(target_links):
    wb.get(PATH_CHROMIUM).open(URL_LOGIN)

    time.sleep(25)

    for i, url in enumerate(target_links):
        wb.get(PATH_CHROMIUM).open_new_tab(url)
        time.sleep(1.5)

    # kill browser with all open windows
    time.sleep(10)
    os.system(CMD_KILL_CHROMIUM)
# ------------------------------------------------------------------------------------

# create new logger
log = Log()

# open new browser window
browser = driver.Chrome(PATH_CHROME_DRIVER)
# login to page
browser.get(URL_LOGIN)
# login delay
time.sleep(2)
# navigate to main page
browser.get(URL_BROWSE)
# find number of pages available
get_last_page_num()
# close existing chromium
browser.quit()

#---------------------------------------------------------
# iterate all pages, get all targets per page
while current_page <= last_page:

    # clear dictionary for each iteration
    dPageTargets.clear()
    # open new browser window
    browser = driver.Chrome(PATH_CHROME_DRIVER)
    # login to page
    browser.get(URL_LOGIN)
    # login delay
    time.sleep(2)
    # navigate to main page
    browser.get(URL_BROWSE)

    # only get BATCH_SIZE number of pages at a time
    for i in range(BATCH_SIZE):        
        # navigate to current page
        url = URL_BASE_PAGE + str(current_page)
        log.log(url)
        browser.get(url)
        # get targets on page
        target_links = get_target_links()
        # load targets into dictionary by page num
        dPageTargets[current_page] = target_links
        # increment page number
        current_page += 1
        
    # close existing chromium
    browser.quit()

    # iterate through target links for each page
    # dictionary contains all links for BATCH_SIZE number of pages
    for page, target_list in dPageTargets.items():
        # display current page
        print("page: " + str(page))
        # process targets on page
        process_targets(target_list)
#---------------------------------------------------------
