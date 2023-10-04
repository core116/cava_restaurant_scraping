"""
This is a web scraper for Cava Restaurants 
"""

# Importing required modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import json
import time
import undetected_chromedriver as uc 
from datetime import datetime

# Get current date 
current_date = datetime.now().date()

driver = uc.Chrome() 

# chrome_options = Options()
# # chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("−−lang=en-US")
# driver = webdriver.Chrome(chrome_options)
# driver.maximize_window()

driver.get("https://cava.com/api/store/nearest/Austin")

try:
    wait = WebDriverWait(driver, 3) # Sets a wait time for driver before throwing an exception
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/pre'))) # Waits till the element with specified class name appears on the page
    address_list = driver.find_element(By.XPATH, '/html/body/pre')
except Exception as e:
    print(e)
    exit()

address_list_json = json.loads(address_list.text)

if len(address_list_json) == 0:
    print("can't find the locatoin")
    exit()    

store_number = address_list_json[0]['storeNumber']

driver.get(f'https://cava.com/api/menu/{store_number}/Pickup')
wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/pre'))) # Waits till the element with specified class name appears on the page
menu_list = driver.find_element(By.XPATH, '/html/body/pre')

menu_list_json = json.loads(menu_list.text)

menu_category_list = menu_list_json['menuData']['categories']


output_data = [['item_id','company_name','item_name','protein_option','price','description','added_date', 'last_modified_date', 'discontinued_date']]

for menu_category in menu_category_list:
    if len(menu_category['choices']) == 0:
        continue
    for sub_product in menu_category['choices']:
        prod_id = sub_product['product_id']
        prod_detail = [pdata for pdata in menu_list_json['productMap'] if pdata['productId'] == prod_id]
        item_id = len(output_data)
        output_data.append([item_id, 'Cava', prod_detail[0]['product']['display_text']['digital_short_name']['en'], '', sub_product['price']['currencies']['USD'], prod_detail[0]['product']['display_text']['digital_long_description']['en'], current_date, current_date, 'none'])

with open('cava.csv', 'w', newline='', encoding='utf-8') as file:
    # Create a writing object
    writer = csv.writer(file)

    # Write output data to the CSV file
    writer.writerows(output_data)

exit()