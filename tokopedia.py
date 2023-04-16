import time
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from scraper import Scraper

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