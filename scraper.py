# E-Commerce Web Scraper
# Created by Daniel Andrew

# Script Use Args: python3 scraper.py <TOKOPEDIA|BHINNEKA|SHOPEE> <search_link> <max_page>

import sys
from datetime import datetime
from selenium import webdriver
import pandas as pd

from tokopedia import TokopediaScraper

class Scraper:
    def __init__(self, web_service=sys.argv[1], page_url=sys.argv[2], max_page=sys.argv[3]):
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

if __name__ == '__main__':
    if sys.argv[1] == 'TOKOPEDIA':
        tokopedia = TokopediaScraper()
        tokopedia.scrape()
        tokopedia.export_to_csv()
        tokopedia.close_driver()
    elif sys.argv[2] == 'BHINNEKA':
        pass
    else:
        pass