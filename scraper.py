# E-Commerce Web Scraper
# Created by Daniel Andrew

# Script Use Args: python3 scraper.py <TOKOPEDIA|BHINEKA|SHOPEE> <search_link> <max_page>

import sys
import time
import requests
from datetime import datetime
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Scraper:
    def __init__(self, web_service=sys.argv[1], page_url=sys.argv[2], max_page=sys.argv[3]):
        self.session = requests.Session()
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.79'}
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.web_service = web_service
        self.page_url = page_url
        self.max_page = max_page
        self.scraped_data = []
        self.soup = None
    
    def scrape(self):
        raise NotImplementedError()
    
    def export_to_csv(self):
        exported_data = pd.DataFrame(self.scraped_data, index=None, columns=['Product Name', 'Product Price', 'Seller', 'Seller Location', 'Sold Products', 'Rating', 'Datetime Scraped'])
        print(exported_data)
        filename = "{web}_DATA_SCRAPING_{date}".format(web=self.web_service, date=datetime.now())
        exported_data.to_csv(filename)
    
    def close_driver(self):
        self.driver.quit()

class TokopediaScraper(Scraper):
    def scrape(self):
        try:
            self.driver.get(self.page_url)
        except Exception as e:
            print(e)
            return
        
        for i in range(int(self.max_page)):
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#zeus-root')))
            time.sleep(2)

            for horizontal_skip in range(30):
                self.driver.execute_script('window.scrollBy(0, 300)')
                time.sleep(0.1)
            
            # Execute Vertical Scrolling to attempt to find pagination
            self.driver.execute_script('window.scrollBy(50, 0)')
            time.sleep(0.5)

            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            product_name = ''
            product_price = ''
            product_seller = ''
            product_seller_loc = ''
            product_total_sold = ''
            product_rating = ''

            for item in self.soup.findAll('div', class_='css-974ipl'):
                product_scraped_timestamp = datetime.now()

                product_name = item.find('div', class_='prd_link-product-name css-3um8ox').text
                product_price = item.find('div', class_='prd_link-product-price css-1ksb19c').text

                for seller_info in item.findAll('div', class_='css-1rn0irl'):
                    if seller_info.findAll('span', class_='css-1kdc32b')[0] != None and seller_info.findAll('span', class_='css-1kdc32b')[1] != None:
                        product_seller = seller_info.findAll('span', class_='css-1kdc32b')[1].text
                        product_seller_loc = seller_info.findAll('span', class_='css-1kdc32b')[0].text
                    else:
                        continue

                for seller_rating_info in item.findAll('div', class_='css-q9wnub'):
                    if seller_rating_info.find('span', class_='css-t70v7i') != None and seller_rating_info.find('span', class_='css-1duhs3e') != None:
                        product_rating = seller_rating_info.find('span', class_='css-t70v7i').text
                        product_total_sold = seller_rating_info.find('span', class_='css-1duhs3e').text
                    else:
                        continue
            
                self.scraped_data.append((product_name, product_price, product_seller, product_seller_loc, product_total_sold, product_rating, product_scraped_timestamp))

            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']").click()
            time.sleep(2)

class BhinekaScraper(Scraper):
    pass

if __name__ == '__main__':
    if sys.argv[1] == 'TOKOPEDIA':
        tokopedia = TokopediaScraper()
        tokopedia.scrape()
        tokopedia.export_to_csv()
        tokopedia.close_driver()
    elif sys.argv[2] == 'BHINEKA':
        pass
    else:
        pass