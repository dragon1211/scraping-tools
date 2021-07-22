
import os
import webbrowser
import time
from datetime import date
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import tkinter as tk
import tkinter.font as font



"""
    Step1: Open the browser
    Step2: Search for the product 
    Step3: Extract the html content of all the products
    Step4: Extract the product description, price, ratings, reviews count and URL
    Step5: Record the product information in a product record list
    Step6: Repeat for all the pages
    Step7: Close the browser
    Step8: Write all the product's information in the product record list in the spreadsheet
"""
site_url = "https://www.wine-searcher.com"

class AmazonProductScraper:
    def __init__(self):
        self.driver = None
        self.rel_cnt = 0
        self.category_name = None
        self.formatted_category_name = None
        self.cur_url = ''
        self.home_url = ''
        self.page_results = ''
        self.content = ''
        self.number_of_pages = 0
        self.result_records = []
        self.urls = list()

    def open_browser(self, search_key):
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("--disable-extensions")
        opt.add_argument('--log-level=OFF')
        opt.add_argument("window-size=400,500")
        opt.add_argument("--start-maximized")
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.cur_url = site_url + "/biz/all"
        self.home_url = site_url + "/biz/all"
        self.urls.append("https://www.julian-fashion.com/en-JP/products/search?searchKey={}".format(search_key))
        self.urls.append("https://www.angelominetti.it/en/shop.html?tp=search&QCerca={}&idsett=man".format(search_key))
        self.urls.append("https://www.viettishop.com/it/catalogsearch/result/?q={}".format(search_key))
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt)
        webbrowser.open_new('')
        for url in self.urls:
            webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open(url)       
        print(self.urls)


    def get_category_url(self):
        category_url = site_url + "/biz/all"
        self.cur_url = category_url
        return category_url


    # @get information of current page.
    def extract_webpage_information(self, url):
        self.cur_url = url
        self.driver.get(self.cur_url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.content = soup
        self.page_results = soup.find_all('tr', {'class' : 'wlrwdt'})


    # @get products information in relative page.
    def extract_rel_information(self, rel_url):
        self.rel_driver.get(rel_url)
        self.rel_cnt += 1
        soup = BeautifulSoup(self.rel_driver.page_source, 'html.parser')
        info = soup.find_all('div', {'class' : 'merchant-banner'})
        
        while len(info) == 0:  
            ok = input('Confirm your verification:(y/n)')
            if ok == 'n': self.scrapping_exit()  
            soup = BeautifulSoup(self.rel_driver.page_source, 'html.parser')
            info = soup.find_all('div', {'class' : 'merchant-banner'})

        telephone = soup.find_all('span',{'itemprop' : 'telephone'})[0].text.strip()
        web_site = soup.find_all('span',{'class' : 'btn1-mp-website'})[0].a.get('href')
        param = {'telephone':telephone, 'website':web_site}
        if self.rel_cnt == 10: 
            self.rel_cnt = 0 
            self.rel_driver.close()
            opt = Options()
            opt.add_argument("--disable-infobars")
            opt.add_argument("--disable-extensions")
            opt.add_argument('--log-level=OFF')
            opt.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.rel_driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt)

        return param


    # @get products information in current page.
    def extract_product_information(self):

        while len(self.page_results) == 0:  
            ok = input('Confirm your verification:(y/n)')
            if ok == 'n': self.scrapping_exit
            self.page_results = soup.find_all('tr', {'class' : 'wlrwdt'})
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # for i in range(len(self.page_results)):
        for i in range(0,10):
            item = self.page_results[i]
            #----------------------------------------------------------
            name = item.find_all('td')[0].text.strip()
            address = item.find_all('td')[3].text.strip()
            a = item.a
            rel_url = site_url + a.get('href')
            res = self.extract_rel_information(rel_url) 
            telephone = res['telephone']
            website = res['website']
            #----------------------------------------------------------
            product_information = (name, address, telephone, website)
            self.result_records.append(product_information)


    def navigate_to_other_pages(self):
        # Contains the list of all the product's information
        self.extract_product_information()
        print("\n>> Page 1 - webpage information extracted")

        # for i in range(2, 5):
        #     next_page_url = site_url + "/biz/all?s=" + str((i-1)*25+1)
        #     self.extract_webpage_information(next_page_url)
        #     self.extract_product_information()
        #     extraction_information = ">> Page {} - webpage information extracted"
        #     print(extraction_information.format(i))

        # self.driver.close()
        # print("\n>> Creating an excel sheet and entering the details...")


    def product_information_spreadsheet(self, records):

        today = date.today().strftime("%d-%m-%Y")
        for _ in records:
            file_name = "{}_{}.csv".format(self.category_name, today)
            f = open(file_name, "w", newline='', encoding='utf-8')
            writer = csv.writer(f)
            writer.writerow(['name', 'address','telephone', 'website url'])
            writer.writerows(records)
            f.close()
        message = (">> Information about the product '{}' is stored in {}\n").format(self.category_name, file_name)
        print(message)

       # os.startfile(file_name)

# ////////////////////////////////////////////////////////////////
    def scrapping_start(self):
        self.open_browser()
        self.navigate_to_other_pages()
        self.product_information_spreadsheet(self.result_records)
    def scrapping_exit(self):
        self.driver.close()
        self.rel_driver.close()
        self.product_information_spreadsheet(self.result_records)
        exit(0)
# ////////////////////////////////////////////////////////////////

if __name__ == "__main__":

#     my_amazon_bot = AmazonProductScraper()
#     # my_amazon_bot.scrapping_start()
#     my_amazon_bot.open_browser()
    def callback(sv):
        if ent_key.get() == '':
            btn_search['state'] = 'disabled'
        else:
            btn_search['state'] = 'normal' 


    def search():
        my_amazon_bot = AmazonProductScraper()
        search_key = ent_key.get() 
        my_amazon_bot.open_browser(search_key)
        
    window = tk.Tk()
    window.title('Search tool')
    window.geometry('800x550')

    myFont = font.Font(family='Helvetica', size=20, weight='bold')
    frm_entry = tk.Frame(master=window)
    sv = tk.StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
    ent_key = tk.Entry(frm_entry, font = myFont, width=20, textvariable=sv)
    lbl_temp = tk.Label(master=frm_entry,font = myFont,  text="キーを入力してください:")

    lbl_temp.grid(row=0, column=0, sticky="w")
    ent_key.grid(row=0, column=1, sticky="e")

    btn_search = tk.Button(
        master=window,
        text="探す",
        command = search,
        font = "Helvetica 15 bold"
    )
    btn_search['state'] = "disabled"
    frm_entry.grid(row=0, column=0, padx=20)
    btn_search.grid(row=0, column=1, pady=15, padx=20)
    
    window.mainloop() 