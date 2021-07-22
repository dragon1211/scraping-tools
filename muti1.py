# import requests
# from bs4 import BeautifulSoup
# from time import sleep

# base_url = 'http://quotes.toscrape.com/page/'

# all_urls = list()

# def generate_urls():
#     for i in range(1,11):
#         all_urls.append(base_url + str(i))
    
# def scrape(url):
#     res = requests.get(url)
#     print(res.status_code, res.url)

# generate_urls()
# for url in all_urls:
#     scrape(url)
###########################################################################################
from multiprocessing import Pool
import requests
# from bs4 import BeautifulSoup

base_url = 'http://quotes.toscrape.com/page/'

all_urls = list()

def generate_urls():
    for i in range(1,11):
        all_urls.append(base_url + str(i))
    
def scrape(url):
    res = requests.get(url)
    print(res.status_code, res.url)

generate_urls()
print(all_urls)

p = Pool(10)
p.map(scrape, all_urls)
p.terminate()
p.join()

# a = input("asdfasdf")

###############################################################
# from multiprocessing import Process
# import os

# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())

# def f(name):
#     info('function f')
#     print('hello', name)

# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()

############Synchronization between processes¶###############
# import os
# import time
# from datetime import date
# import csv
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import NoSuchElementException
# from multiprocessing import Process, Lock


       

# """
#     Step1: Open the browser
#     Step2: Search for the product 
#     Step3: Extract the html content of all the products
#     Step4: Extract the product description, price, ratings, reviews count and URL
#     Step5: Record the product information in a product record list
#     Step6: Repeat for all the pages
#     Step7: Close the browser
#     Step8: Write all the product's information in the product record list in the spreadsheet
# """
# site_url = "https://www.wine-searcher.com"

# class AmazonProductScraper:
#     def __init__(self):
#         self.driver = None
#         self.rel_cnt = 0
#         self.category_name = None
#         self.formatted_category_name = None
#         self.cur_url = ''
#         self.home_url = ''
#         self.page_results = ''
#         self.content = ''
#         self.number_of_pages = 0
#         self.result_records = []

#     def open_browser(self):
#         opt = Options()
#         opt.add_argument("--disable-infobars")
#         opt.add_argument("--disable-extensions")
#         opt.add_argument('--log-level=OFF')
#         opt.add_experimental_option('excludeSwitches', ['enable-logging'])
#         self.cur_url = site_url + "/biz/all"
#         self.home_url = site_url + "/biz/all"
#         # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt)
        

#         search_key = input('Input your product key:')
        
#         # url1 = "https://www.gebnegozionline.com/it_it/"
#         url2 = "https://www.julian-fashion.com/en-JP/products/search?searchKey={}"
#         url3 = "https://www.angelominetti.it/en/shop.html?tp=search&QCerca={}&idsett=man"
#         url4 = "https://www.viettishop.com/it/catalogsearch/result/?q={}"

#         # url1 = url1.format(search_key)
#         url2=  url2.format(search_key)
#         url3 = url3.format(search_key)
#         url4 = url4.format(search_key)

#         # driver1.get(url1)
#         # time.sleep(3)

#         driver2 = webdriver.Chrome(ChromeDriverManager().install(), options=opt)
#         driver2.get(url2)
#         time.sleep(3)

#         driver3 = webdriver.Chrome(ChromeDriverManager().install(), options=opt)
#         driver3.get(url3)
#         time.sleep(3)

#         driver4 = webdriver.Chrome(ChromeDriverManager().install(), options=opt)
#         driver4.get(url4)




# def f(l, i):
#     l.acquire()
#     A = AmazonProductScraper()
#     A.open_browser()
#     try:
#         print('hello world', i)
#     finally:
#         l.release()

# if __name__ == '__main__':
#     lock = Lock()

#     for num in range(10):
#         Process(target=f, args=(lock, num)).start()
