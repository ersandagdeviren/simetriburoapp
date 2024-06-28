#!/usr/bin/env python
# coding: utf-8

# In[26]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure webdriver options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the webdriver using webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), ) #options=chrome_options

try:
    # Open the login page
    driver.get('https://portal.smartdonusum.com/accounting/login')

    # Locate the username and password fields
    username_field = driver.find_element(By.CSS_SELECTOR, '#username')
    password_field = driver.find_element(By.CSS_SELECTOR, '#password')

    # Enter the username and password
    username_field.send_keys('admin_005256')
    password_field.send_keys('x&2U*bnD')
    # Submit the form
    password_field.send_keys(Keys.RETURN)

    # Wait for the login process to complete
    time.sleep(5)

    # Click on the specified elements
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#style-7 > ul > li:nth-child(5) > a'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#pagesTransformation > ul > li:nth-child(1) > a'))).click()

    # Wait for the input field to be visible and send the number
    input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#react-select-4--value > div.Select-input > input')))
    input_field.send_keys('6340441483')
    time.sleep(3)
    input_field.send_keys(Keys.TAB) 
    
    item_name_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#itemName_0')))
    item_name_field.send_keys('Sample Item')
    item_name_field.send_keys(Keys.TAB)
    item_name_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#quantity_0')))
    item_name_field.send_keys('12')
    item_name_field.send_keys(Keys.TAB)
    item_name_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#unitPrice_0')))
    item_name_field.send_keys('100')
    item_name_field.send_keys(Keys.TAB)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#react > div > div:nth-child(1) > div.wrapper > div.main-panel > div.content > div > div.col-sm-12.satirBasi > div.col-sm-12.baseDashboard > div > div.card-header > div > div.col-sm-9 > div > div:nth-child(2) > button'))).click()
    


    # Optional: W    #react > div > div:nth-child(1) > div.wrapper > div.main-panel > div.content > div > div.col-sm-12.satirBasi > div.col-sm-12.baseDashboard > div > div.card-body > div > div > table > tbody > tr > td.form-group > div
finally:
    # Close the browser
    pass


# In[ ]:


username_field.send_keys('admin_005256')
password_field.send_keys('x&2U*bnD')


# In[ ]:


#style-7 > ul > li:nth-child(5) > a

