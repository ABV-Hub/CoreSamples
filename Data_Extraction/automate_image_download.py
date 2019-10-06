from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time


# launch web browser
browser = webdriver.Firefox()

# wait for browser to load
# time.sleep(10)

# go to IODP site
browser.get('http://web.iodp.tamu.edu/LORE/')

# select "Images" menu item
browser.execute_script("document.getElementById('MENU101').click()")
# select "Core Sections"
browser.execute_script("document.getElementById('MENU99121').click()")
# select "Standard"
browser.execute_script("document.getElementById('MENU121').click()")

# select expedition
browser.execute_script("document.getElementsByClassName('ui-multiselect ui-widget ui-state-default ui-corner-all')[0].click()")
browser.execute_script("document.getElementById('ui-multiselect-SEARCH_MODULE_expedition-option-49').click()")

# pick site
browser.execute_script("document.getElementsByClassName('ui-multiselect ui-widget ui-state-default ui-corner-all')[1].click()")
browser.execute_script("document.getElementById('ui-multiselect-SEARCH_MODULE_site-option-3').click()")

# select hole
selectHole = browser.find_element_by_id("SEARCH_MODULE_hole")
selectHole.send_keys('A')

# select core
selectCore = browser.find_element_by_id("SEARCH_MODULE_core")
selectCore.send_keys('1')


# pick types
browser.execute_script("document.getElementsByClassName('ui-multiselect ui-widget ui-state-default ui-corner-all')[2].click()")
browser.execute_script("document.getElementById('ui-multiselect-SEARCH_MODULE_type-option-0').click()")


# show data
browser.execute_script("document.getElementById('showReportButton').click()")

# download files
browser.execute_script("document.getElementById('downloadFiles').click()")

# select cropped images
#browser.execute_script("document.getElementByName('ui-multiselect-SEARCH_MODULE_expedition-option-49').click()")


# select default link for uncropped images
browser.execute_script("document.getElementById('picklink').click()")

#browser.close()

