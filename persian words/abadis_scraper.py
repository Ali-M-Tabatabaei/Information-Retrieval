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
num_threads = 5
max_depth = 2
start_urls = ["https://abadis.ir/amid"]  # Add initial URLs here

# Setting up Selenium WebDriver
options = webdriver.ChromeOptions()
# option.add_argument("start-maximized")
options.add_experimental_option("detach", True)

options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Queue to hold URLs
url_queue = Queue()

# Lock for print statements
print_lock = threading.Lock()


class Scraper:
    def __init__(self):
        # Configuration
        self.num_threads = 5
        self.max_depth = 2
        self.start_urls = ["https://abadis.ir/amid"]  # Add initial URLs here

        # Setting up Selenium WebDriver
        self.options = webdriver.ChromeOptions()
        # option.add_argument("start-maximized")
        self.options.add_experimental_option("detach", True)

        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Queue to hold URLs
        self.url_queue = Queue()

        # Lock for print statements
        self.print_lock = threading.Lock()

    # Producer thread
    class Producer(threading.Thread):
        def __init__(self, urls):
            threading.Thread.__init__(self)
            self.urls = urls

        def run(self):
            for url in self.urls:
                url_queue.put((url, 0))  # (url, depth)

    # Consumer thread
    class Consumer(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.driver = driver

        def run(self):
            while True:
                url, depth = url_queue.get()
                if depth <= max_depth:
                    self.scrape(url, depth)
                url_queue.task_done()

        def scrape(self, url, depth):
            with print_lock:
                print(f"Scraping: {url} at depth: {depth}")
            self.driver.get(url)
            time.sleep(2)  # Let the page load

            # Add custom scraping logic here (e.g., extracting links, data)
            try:
                links = self.driver.find_elements(By.TAG_NAME, "a")
                for link in links:
                    href = link.get_attribute("href")
                    if href and href.startswith("http"):
                        url_queue.put((href, depth + 1))
            except Exception as e:
                with print_lock:
                    print(f"Error scraping {url}: {e}")

        def quit(self):
            self.driver.quit()

    def get_starting_urls(self):
        urls = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 'body > main > div:nth-child(5) > div'))
        )
        print(urls)


# Main script
if __name__ == "__main__":
    scraper = Scraper()
    scraper.get_starting_urls()
    # Start producer
    # producer = Producer(start_urls)
    # producer.start()
    # producer.join()
    #
    # # Start consumers
    # consumers = []
    # for _ in range(num_threads):
    #     consumer = Consumer()
    #     consumer.start()
    #     consumers.append(consumer)
    #
    # # Wait for the queue to be empty
    # url_queue.join()
    #
    # # Quit all drivers
    # for consumer in consumers:
    #     consumer.quit()
