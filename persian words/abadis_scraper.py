import re
import threading
from queue import Queue
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# Configuration
# num_threads = 5
# max_depth = 2
# start_urls = ["https://abadis.ir/amid"]  # Add initial URLs here

# Setting up Selenium WebDriver
# options = webdriver.ChromeOptions()
# option.add_argument("start-maximized")
# options.add_experimental_option("detach", True)

# options.add_argument("--headless")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Queue to hold URLs
# url_queue = Queue()

# Lock for print statements
# print_lock = threading.Lock()


class Scraper:
    def __init__(self):
        # Configuration
        self.producer = None
        self.consumer = None
        self.num_threads = 5
        self.max_depth = 2
        self.start_urls = ["https://abadis.ir/amid"]  # Add initial URLs here
        self.pattern1 = r'https://abadis.ir/amid/?ch=*'  # Pattern for depth 1 URLs
        self.pattern2 = r'https://abadis.ir/fatofa/*'  # Pattern for hrefs in depth 2
        # Setting up Selenium WebDriver
        self.options = webdriver.ChromeOptions()
        # option.add_argument("start-maximized")
        self.options.add_experimental_option("detach", True)

        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.get("https://abadis.ir/amid")
        self.scraped_data = []
        # Queue to hold URLs
        self.url_queue = Queue()
        # Lock for print statements
        self.print_lock = threading.Lock()

    # Producer thread
    class Producer(threading.Thread):
        def __init__(self, urls, scraper_instance):
            threading.Thread.__init__(self)
            self.urls = urls
            self.scraper = scraper_instance

        def run(self):
            for url in self.urls:
                scraper.url_queue.put((url, 1))  # (url, depth)

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

            # Custom scraping logic
            if depth == 1:
                self.scrape_depth1(url)
            elif depth == 2:
                self.scrape_depth2(url)
            else:
                pass

        def scrape_depth1(self, url):
            # body > main > div.boxBd > div.boxLi > a
            urls = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                     'body > main > div.boxBd > div.boxLi > a'))
            )
            for url in urls:
                href = url.get_attribute('href')
                # if href and re.search(scraper.pattern1, href):
                scraper.url_queue.put((href, 2))
                print(href)

        def scrape_depth2(self, url):
            links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if href and re.search(scraper.pattern2, href):
                    data = {
                        "depth1_url": url,
                        "depth2_href": href,
                        "text": link.text
                    }
                    with scraper.print_lock:
                        scraper.scraped_data.append(data)

        def quit(self):
            self.driver.quit()

    def get_starting_urls(self):
        urls = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 'body > main > div:nth-child(5) > div > a'))
        )
        urls = [url.get_attribute('href') for url in urls]
        self.producer = self.Producer(urls=urls, scraper_instance=self)
        self.consumer = self.Consumer(scraper_instance=self)

    def url_chain(self):
        # Start producer
        self.producer.start()
        self.producer.join()
        #
        # Start consumers
        consumers = []
        for _ in range(self.num_threads):
            self.consumer.start()
            consumers.append(self.consumer)

        # Wait for the queue to be empty
        self.url_queue.join()

        # Quit all drivers
        for consumer in consumers:
            consumer.quit()


# Main script
if __name__ == "__main__":
    scraper = Scraper()
    scraper.get_starting_urls()
    scraper.url_chain()
    print(scraper.scraped_data)
