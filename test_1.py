# import libraries
from bs4 import BeautifulSoup
# import numpy as np
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep
from random import randint
from selenium import webdriver

from datetime import date
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
###########################
# Loop of all the pages
###########################

#Loop to go over all pages
# pages = np.arange(1, 3, 1)
data=[]

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("--disable-extensions")
opt.add_argument('--log-level=OFF')
opt.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt)

for page in range(1, 10):
    
    page="https://www.hostelworld.com/s?q=Barcelona,%20Catalonia,%20Spain&country=Spain&city=\
            Barcelona&type=city&id=83&from=2020-07-03&to=2020-07-05&guests=1&page=" + str(page) 
  
    driver.get(page)  
    sleep(randint(2,10))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    my_table = soup.fin #
    for tag in my_table:
        data.append(tag.get_text())