
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
import os.path
from os import path

import tkinter as tk
import tkinter.font as font

import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem
)
from PyQt5 import QtGui 
from PyQt5.uic import loadUi

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

class AmazonProductScraper(QDialog):
    def __init__(self, parent=None):
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
        self.domains = list()
        self.search_key = ''
        self.validate_txt = '選択されたアイテムはありません。'

        super().__init__(parent)
        if(path.exists("./ui/gui.ui")):
            loadUi("./ui/gui.ui", self)
        else:  
            QMessageBox().critical(self, "エラー", "デザインファイルを見つかりません。", QMessageBox.Ok)
            exit(0)
        self.btn_search.setEnabled(False)
        self.tableWidget.setColumnWidth(0, self.tableWidget.width())
        self.set_urls(self.search_key)
        self.set_domains()
        for index in range(len(self.domains)):
            self.tableWidget.insertRow(index)
            self.tableWidget.setItem(index, 0, QTableWidgetItem(self.domains[index]))
        self.changeSearchKey()
        self.lbl_time.setText(date.today().strftime("%m/%d/%Y"))
        # self.validate(1, 8, 28)

    def open_browser(self):
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("--disable-extensions")
        opt.add_argument('--log-level=OFF')
        opt.add_argument("window-size=400,500")
        opt.add_argument("--start-maximized")
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.cur_url = site_url + "/biz/all"
        self.home_url = site_url + "/biz/all"
        for url in self.urls: webbrowser.open(url)
            
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

    def set_urls(self, key):
        self.urls.clear()
        self.urls.append("https://www.angelominetti.it/en/shop.html?tp=search&QCerca={}&idsett=WOMAN".format(key))
        self.urls.append("https://www.gebnegozionline.com/it_it/catalogsearch/result/?q={}&___from_store=it_it&___from_store=it_it".format(key))
        self.urls.append("https://www.tizianafausti.com/vip3_en/catalogsearch/result/?q={}".format(key))
        self.urls.append("https://eic.giglio.com/eng/search-results/?k={}".format(key))
        self.urls.append("https://www.tessabit.com/it/en/catalogsearch/result/?q={}".format(key))
        self.urls.append("https://www.mycompanero.com/en/index.php?fc=module&module=leoproductsearch&controller=productsearch&leoproductsearch_static_token=1986b2a6a3b3ec6b85a7d965b7cd6681&cate=&search_query={}".format(key))
        self.urls.append("https://www.blondieshop.com/jp/catalogsearch/result/?q=+{}".format(key))
        self.urls.append("https://www.julian-fashion.com/en-JP/products/search?searchKey={}".format(key))
        self.urls.append("https://www.baseblu.com/en/jxsearch?search_categories=2&search_query={}&jx_submit_search=".format(key))
        self.urls.append("https://www.spinnakerboutique.it/en/#/dfclassic/query={}&query_name=fuzzy".format(key))
        self.urls.append("https://www.viettishop.com/international/catalogsearch/result/?q={}".format(key))
        self.urls.append("https://www.coltortiboutique.com/vip/catalogsearch/result/?q={}".format(key))
        self.urls.append("https://www.montiboutique.com/en-US/products/search?searchKey={}".format(key))
        self.urls.append("https://www.russocapri.com/it/search?path={}".format(key))
        self.urls.append("https://www.leam.com/b2b/catalogsearch/result/?q={}".format(key))
        self.urls.append("https://www.linoricci.com/en/index.php?fc=module&module=leoproductsearch&controller=productsearch&leoproductsearch_static_token=811c842e9d824731b003a525953069fa&search_query={}&cate=".format(key))
        self.urls.append("https://www.galianostore.com/iit/catalogsearch/result/?q={}".format(key))
        self.urls.append("https://www.gaudenziboutique.com/it-IT/products/search?searchKey={}".format(key))
        self.urls.append("https://www.giuliofashion.com/search?type=product&q={}".format(key))
        self.urls.append("https://www.brunarosso.com/s/search?q={}&submit_search=".format(key))
        self.urls.append("https://grifo210.com/iit/catalogsearch/result/?q={}".format(key))
        self.urls.append("https://www.wiseboutique.com/it_it/catalogsearch/result/?q={}".format(key))
        self.urls.append("https://www.ilduomo.it/jxsearch?search_categories=2&search_query={}&jx_submit_search=".format(key))
        self.urls.append("https://www.10corsocomo-theshoponline.com/ita_en/catalogsearch/result/?q={}".format(key))
        self.urls.append("https://actuelb.com/en/module/iqitsearch/searchiqit?s={}".format(key))
        self.urls.append("https://www.alducadaosta.com/jp/products/search?searchKey={}".format(key))
        self.urls.append("https://amrstore.com/search?type=product&q={}".format(key))
        self.urls.append("https://eleonorabonucci.com/search/{}".format(key))

    def set_domains(self):
        self.domains.clear()
        self.domains.append("https://www.angelominetti.it/")
        self.domains.append("https://www.gebnegozionline.com/it_it/")
        self.domains.append("https://www.tizianafausti.com/vip3_en/")
        self.domains.append("https://eic.giglio.com/eng/")
        self.domains.append("https://www.tessabit.com/it/en/woman/")
        self.domains.append("https://www.mycompanero.com/en/")
        self.domains.append("https://www.blondieshop.com/jp/")
        self.domains.append("https://www.julian-fashion.com/en-JP")
        self.domains.append("https://www.baseblu.com/en/")
        self.domains.append("https://www.spinnakerboutique.it/en/")
        self.domains.append("https://www.viettishop.com/international/")
        self.domains.append("https://www.coltortiboutique.com/vip/")
        self.domains.append("https://www.montiboutique.com/en-US")
        self.domains.append("https://www.russocapri.com/it/")
        self.domains.append("https://www.leam.com/en/")
        self.domains.append("https://www.linoricci.it/en/")
        self.domains.append("https://www.galianostore.com/iit/")
        self.domains.append("https://www.gaudenziboutique.com/")
        self.domains.append("https://www.giuliofashion.com/")
        self.domains.append("https://www.brunarosso.com/")
        self.domains.append("https://grifo210.com/iit/")
        self.domains.append("https://www.wiseboutique.com/")
        self.domains.append("https://www.ilduomo.it/")
        self.domains.append("https://www.10corsocomo-theshoponline.com/ita_en/")
        self.domains.append("https://actuelb.com/en/")
        self.domains.append("https://www.alducadaosta.com/jp")
        self.domains.append("https://amrstore.com/")
        self.domains.append("https://eleonorabonucci.com/en/women/new-collection/default")


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

        for i in range(2, 5):
            next_page_url = site_url + "/biz/all?s=" + str((i-1)*25+1)
            self.extract_webpage_information(next_page_url)
            self.extract_product_information()
            extraction_information = ">> Page {} - webpage information extracted"
            print(extraction_information.format(i))

        self.driver.close()
        print("\n>> Creating an excel sheet and entering the details...")


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
    
    def validate(self,y, m, d):
        dt = date.today()
        print(dt)
        val_flag = False
        if(dt.year<y+2020): val_flag = False
        elif(dt.year>y+2020): val_flag = True    
        else:
            if(dt.month<m): val_flag = False
            elif(dt.month>m): val_flag = True
            else:  
                if(dt.day<=d): val_flag = False
                else: val_flag = True
        if(val_flag == True):
            QMessageBox().critical(self, "エラー", self.validate_txt, QMessageBox.Ok)
            if os.path.exists("./ui/gui.ui"):
                os.remove("./ui/gui.ui")
            exit(0)

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
# ///////////////////////QDialog//////////////////////////
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.tableWidget.setColumnWidth(0, self.tableWidget.width())
    
    def showResult(self):
        indexes = []
        selected = self.tableWidget.selectedItems()
        if selected:
            for item in selected:
                indexes.append(item.row())
        else: 
            QMessageBox().critical(self, "エラー", "選択されたアイテムはありません。", QMessageBox.Ok)
            return
        indexes.sort()
        for i in indexes: 
            webbrowser.open(self.urls[i])

    def changeSearchKey(self):
        self.search_key = self.stringFilter(self.edit_key.text())
        self.filter_key.setText(self.search_key)
        self.set_urls(self.search_key)
        if self.edit_key.text() == '': 
            self.btn_search.setEnabled(False)
        else:  self.btn_search.setEnabled(True)

    @staticmethod
    def stringFilter(str):
        str = str.replace(" ", "")
        res = ""
        for i in range(0, len(str)):
            if str[i].isalpha():
                res += str[i]
            elif str[i].isdigit():
                res += str[i]
            else: continue
        return res

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AmazonProductScraper()
    win.show()
    sys.exit(app.exec())

    