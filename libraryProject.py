# -*- coding = utf-8 -*-
# @Time : 8/28/2022 6:04 PM
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import common

my_list = pd.read_csv('Copy of Gift titles - Claim task - PO Line + Fund.csv')
po_list = []
for i in range(len(my_list)):
    po_list.append(my_list['PO#'][i])

receiving_note = []

chrome_option = webdriver.ChromeOptions()
chrome_option.add_argument(r"user-data-dir=C:\\selenium")
driver = webdriver.Chrome(options=chrome_option)
driver.get("https://na01.alma.exlibrisgroup.com/mng/login?institute=01UMN_INST&auth=SAML")
my_username = "#"
my_password = "#"
username = driver.find_element_by_id("username")
username.send_keys(my_username)
password = driver.find_element_by_id("password")
password.send_keys(my_password)
form = driver.find_element_by_id('main-content')
submit_button = form.find_element(by=By.XPATH, value=".//*[@type='submit']")
submit_button.click()

WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='duo_iframe']")))
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Send Me a Push']"))).click()
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Receive'))).click()
WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "find_poLineList")))

for i in range(len(po_list)):
    search = driver.find_element_by_id("find_poLineList")
    search.clear()
    search.send_keys(po_list[i])
    search.send_keys(Keys.ENTER)
    time.sleep(3)
    note = ""
    try:
        driver.find_element_by_xpath("//*[@id='SELENIUM_ID_poLineList_ROW_0_COL_poLinepoLineReference']/a/mark").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "// *[ @ id = 'PAGE_BUTTONS_acqbuttonEdit']"))).click()
        time.sleep(5)

        my_text = driver.find_element_by_xpath("// *[ @ id = 'pageBeanpoLinereceivingNote']")
        receiving_note.append(my_text.text)
        my_text.send_keys(my_list['String'][i])
        time.sleep(4)
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='PAGE_BUTTONS_save_full_validation']"))).click()
    except common.exceptions.NoSuchElementException:
        receiving_note.append(str(po_list[i]) + "Error")
        break
    finally:
        time.sleep(4)
        series = pd.Series(receiving_note)
        series.to_csv('receivingNote6.csv', index=False)
