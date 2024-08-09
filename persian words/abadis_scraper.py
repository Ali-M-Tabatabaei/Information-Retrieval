import re
import threading
from queue import Queue

import selenium.common.exceptions
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import json


class Scraper:
    def __init__(self, file):
        # Configuration
        self.file = file
        self.producer = None
        self.consumers = []
        self.num_threads = 1
        self.max_depth = 2
        self.start_urls = ["https://abadis.ir/amid"]  # Add initial URLs here
        self.pattern1 = r'https://abadis.ir/amid/?ch=*'  # Pattern for depth 1 URLs
        self.pattern2 = r'https://abadis.ir/fatofa/*'  # Pattern for hrefs in depth 2
        # Setting up Selenium WebDriver
        self.options = webdriver.ChromeOptions()
        # option.add_argument("start-maximized")
        self.options.add_experimental_option("detach", True)

        # self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.get("https://abadis.ir/amid")
        self.scraped_data = []
        # Queue to hold URLs
        self.url_queue = Queue()
        # Lock for print statements
        self.print_lock = threading.Lock()

    # Producer thread
    class Producer(threading.Thread):
        def __init__(self, urls, scraper_instance, initial_depth):
            threading.Thread.__init__(self)
            self.urls = urls
            self.scraper = scraper_instance
            self.initial_depth = initial_depth

        def run(self):
            for url in self.urls:
                scraper.url_queue.put((url, self.initial_depth))  # (url, depth)

    # Consumer thread
    class Consumer(threading.Thread):
        def __init__(self, scraper_instance):
            threading.Thread.__init__(self)
            self.scraper = scraper_instance
            self.driver = scraper.driver

        def run(self):
            while True:
                url, depth = scraper.url_queue.get()
                if depth <= scraper.max_depth:
                    self.scrape(url, depth)
                scraper.url_queue.task_done()

        def scrape(self, url, depth):
            with scraper.print_lock:
                print(f"Scraping: {url} at depth: {depth}")
            self.driver.get(url)
            # time.sleep(2)
            # Custom scraping logic
            if depth == 1:
                self.scrape_depth1(url)
            elif depth == 2:
                self.scrape_depth2(url)
            else:
                pass

        def scrape_depth1(self, url):
            # body > main > div.boxBd > div.boxLi > a
            urls = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                     'body > main > div.boxBd > div.boxLi > a'))
            )
            for link in urls:
                if link.get_attribute('href') is not None:
                    href = link.get_attribute('href')
                    scraper.url_queue.put((href, 2))
                    print(href)
                    scraper.file.write(href)
            page_number = 2
            while page_number != False:
                self.driver.get(url + f'&pn={page_number}')
                if self.driver.current_url.__contains__("lock"):
                    WebDriverWait(self.driver, 3600).until(EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "body > main > div.boxBd > div.boxLi > a")))
                try:
                    scraped_urls = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, 'body > main > div.boxBd > div.boxLi > a')))
                except TimeoutException:
                    page_number = False
                    continue
                for element in scraped_urls:
                    if element is not None and element.get_attribute('href') is not None:
                        href = element.get_attribute('href')
                        scraper.url_queue.put((href, 2))
                        print(href)
                        scraper.file.write(href)

                # time.sleep(0.5)
                page_number += 1
                if page_number == 91:
                    page_number = False

        def scrape_depth2(self, url):
            meaning = ""
            if self.driver.current_url.__contains__("lock"):
                WebDriverWait(scraper.driver, 3600).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#boxWrd > h1"))
                )
            if self.driver.current_url.__contains__("#[fl]"):
                self.driver.get(self.driver.current_url.replace("#[fl]", ""))
            try:
                # ad_button = self.driver.find_element(By.CSS_SELECTOR, "#close-btn")
                ad_button = WebDriverWait(scraper.driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#close-btn"))
                )
                ad_button.click()

            except :
                pass

            title = WebDriverWait(scraper.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#boxWrd > h1"))
            )
            word = title.text
            dictionaries = WebDriverWait(scraper.driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body > main > div"))
            )
            for dictionary in dictionaries:
                if dictionary.text.__contains__("عمید"):
                    WebDriverWait(scraper.driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, ".//div[contains(@class, 'boxHd')]"))
                    ).click()
                    # button.click()
                    text_field = WebDriverWait(scraper.driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, ".//div[contains(@class, 'boxBd boxBdNop')][1]")))
                    meaning = text_field.text
                    print(meaning)

            data = {
                "word": word,
                "meaning": meaning,
                "score": 0
            }
            print(data)
            with scraper.print_lock:
                scraper.scraped_data.append(data)

        def quit(self):
            self.driver.quit()

    def get_starting_urls(self):
        urls = WebDriverWait(self.driver, 60).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 'body > main > div:nth-child(5) > div > a'))
        )
        urls = [url.get_attribute('href') for url in urls]
        self.producer = self.Producer(urls, scraper, 1)

    def url_chain(self):
        # Start consumers
        for _ in range(self.num_threads):
            consumer = self.Consumer(scraper_instance=self)
            self.consumers.append(consumer)
        for cons in self.consumers:
            cons.start()
        # Start producer
        self.producer.start()
        self.producer.join()

        # Wait for the queue to be empty
        self.url_queue.join()

        # Quit all drivers
        for consumer in self.consumers:
            consumer.quit()

    def url_seperator(self):
        with open('urls.txt', 'r') as f:
            line = f.readline().strip()
        urls = ["https://" + part for part in line.split('https://') if part]
        self.producer = self.Producer(urls, scraper, 2)


# Main script
if __name__ == "__main__":
    file = open("urls.txt", "a")
    scraper = Scraper(file)
    # scraper.get_starting_urls()
    scraper.url_seperator()
    scraper.url_chain()
    with open("dictionary.json", "w") as outfile:
        json.dump(scraper.scraped_data, outfile)
    file.close()
