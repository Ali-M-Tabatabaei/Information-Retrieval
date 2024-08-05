# selenium 4
import json

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
global depth

option = webdriver.ChromeOptions()
# option.add_argument("start-maximized")
option.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.get('https://ieeexplore.ieee.org/Xplore/home.jsp')



# Function to handle the cookie consent banner
def handle_cookie_consent():
    try:
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.osano-cm-dialog__buttons.osano-cm-buttons > button.osano-cm-accept-all.osano-cm-buttons__button.osano-cm-button.osano-cm-button--type_accept'))
        )
        consent_button.click()
    except (NoSuchElementException, ElementClickInterceptedException):
        pass
    
    
# searching for paper
def search_paper(query):
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#LayoutWrapper > div > div > div.ng2-app > div > xpl-root > header > xpl-header > div > div.bg-hero-img > div.search-bar-container > xpl-search-bar-migr > div > form > div.search-field > div > div.global-search-bar > xpl-typeahead-migr > div > input'))
    )
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)


def get_result_papers():
    return WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'xpl-results-item > div.hide-mobile > div.d-flex.result-item > div.col.result-item-align.px-3 > h3 > a'))
    )


def get_page():
    try:
        fields = driver.find_elements(By.CSS_SELECTOR, "xpl-document-details > div > "
                                                       "div.document-main.global-content-width-w-rr > div > "
                                                       "div.document-main-content-container.col-19-24 > section > "
                                                       "div.document-main-left-trail-content > div > "
                                                       "xpl-document-abstract > section > "
                                                       "div.abstract-desktop-div.hide-mobile.text-base-md-lh > "
                                                       "div.row.g-0.u-pt-1 > div:nth-child(1) > div")
        for field in fields:
            if field.text.__contains__("Page"):
                return field.text.split(": ")[1]
        return None
    except NoSuchElementException:
        return None


def get_title():
    title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        "xpl-document-details > div > div.document-main.global-content-width-w-rr > "
                                        "section.document-main-header.row.g-0 > div > xpl-document-header > section > "
                                        "div.document-header-inner-container.row.g-0 > div > div > "
                                        "div.row.g-0.document-title-fix > div > div.left-container.w-100 > h1 > span"))
    )
    return title.text


def get_cites_papers():
    cites = 0
    buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                             "xpl-document-details > div > div.document-main.global-content-width-w-rr > "
                                             "section.document-main-header.row.g-0 > div > xpl-document-header > section > "
                                             "div.document-header-inner-container.row.g-0 > div > div > "
                                             "div.document-main-subheader > "
                                             "div.document-header-metrics-banner.d-flex.flex-wrap > "
                                             "div.document-banner.col.stats-document-banner > "
                                             "div.document-banner-metric-container.d-flex > button"))
    )
    for button in buttons:
        if button.text.__contains__("Papers"):
            cites = int(button.text.split('\n')[0])
    return int(cites)


def get_cites_patents():
    num_cites = 0
    if len(driver.find_elements(By.CSS_SELECTOR,
                                "xpl-document-details > div > div.document-main.global-content-width-w-rr > "
                                "section.document-main-header.row.g-0 > div > xpl-document-header > section > "
                                "div.document-header-inner-container.row.g-0 > div > div > "
                                "div.document-main-subheader > div.document-header-metrics-banner.d-flex.flex-wrap > "
                                "div.document-banner.col.stats-document-banner > "
                                "div.document-banner-metric-container.d-flex > button:nth-child(2) > div")) > 2:
        num_cites = driver.find_element(By.CSS_SELECTOR,
                                        "xpl-document-details > div > div.document-main.global-content-width-w-rr > "
                                        "section.document-main-header.row.g-0 > div > xpl-document-header > section > "
                                        "div.document-header-inner-container.row.g-0 > div > div > "
                                        "div.document-main-subheader > "
                                        "div.document-header-metrics-banner.d-flex.flex-wrap > "
                                        "div.document-banner.col.stats-document-banner > "
                                        "div.document-banner-metric-container.d-flex > button:nth-child(2) > "
                                        "div.document-banner-metric-count").text
    return int(num_cites)


def get_full_text_views():
    views = 0
    buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                             "xpl-document-details > div > div.document-main.global-content-width-w-rr > "
                                             "section.document-main-header.row.g-0 > div > xpl-document-header > section > "
                                             "div.document-header-inner-container.row.g-0 > div > div > "
                                             "div.document-main-subheader > "
                                             "div.document-header-metrics-banner.d-flex.flex-wrap > "
                                             "div.document-banner.col.stats-document-banner > "
                                             "div.document-banner-metric-container.d-flex > button"))
    )
    for button in buttons:
        if button.text.__contains__("Views"):
            views = int(button.text.split('\n')[0])
    return int(views)


def get_publisher():
    publisher = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "xpl-document-details > div > "
                                                         "div.document-main.global-content-width-w-rr > div > "
                                                         "div.document-main-content-container.col-19-24 > section > "
                                                         "div.document-main-left-trail-content > div > "
                                                         "xpl-document-abstract > section > "
                                                         "div.abstract-desktop-div.hide-mobile.text-base-md-lh > "
                                                         "div.row.g-0.u-pt-1 > div:nth-child(2) > "
                                                         "div.u-pb-1.doc-abstract-publisher > xpl-publisher > span > span "
                                                         "> span > span:nth-child(2)"))
    ).text
    return publisher


def get_doi():
    try:
        doi = driver.find_element(By.CSS_SELECTOR, "xpl-document-details > div > "
                                                   "div.document-main.global-content-width-w-rr > div > "
                                                   "div.document-main-content-container.col-19-24 > section > "
                                                   "div.document-main-left-trail-content > div > xpl-document-abstract > "
                                                   "section > div.abstract-desktop-div.hide-mobile.text-base-md-lh > "
                                                   "div.row.g-0.u-pt-1 > div:nth-child(2) > "
                                                   "div.u-pb-1.stats-document-abstract-doi > a").text
        return doi
    except NoSuchElementException:
        return None


def get_publication_date():
    try:
        publication_date = driver.find_element(By.CSS_SELECTOR, 'xpl-document-details > '
                                                                'div > div.document-main.global-content-width-w-rr > div '
                                                                '> div.document-main-content-container.col-19-24 > '
                                                                'section > div.document-main-left-trail-content > div > '
                                                                'xpl-document-abstract > section > '
                                                                'div.abstract-desktop-div.hide-mobile.text-base-md-lh > '
                                                                'div.row.g-0.u-pt-1 > div:nth-child(1) > '
                                                                'div.u-pb-1.doc-abstract-confdate').text
    except NoSuchElementException:
        try:

            publication_date = driver.find_element(By.CSS_SELECTOR, 'xpl-document-details '
                                                                    '> div > div.document-main.global-content-width-w-rr '
                                                                    '> div > '
                                                                    'div.document-main-content-container.col-19-24 > '
                                                                    'section > div.document-main-left-trail-content > '
                                                                    'div'
                                                                    '> xpl-document-abstract > section > '
                                                                    'div.abstract-desktop-div.hide-mobile.text-base-md-lh '
                                                                    '> div.row.g-0.u-pt-1 > div:nth-child(1) > '
                                                                    'div.u-pb-1.doc-abstract-pubdate').text
        except NoSuchElementException:
            return None

    return publication_date.split(': ')[1]


def get_abstract():
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "xpl-document-details > div > "
                                                         "div.document-main.global-content-width-w-rr > div > "
                                                         "div.document-main-content-container.col-19-24 > section > "
                                                         "div.document-main-left-trail-content > div > xpl-document-abstract > "
                                                         "section > div.abstract-desktop-div.hide-mobile.text-base-md-lh > "
                                                         "div.abstract-text.row.g-0 > div > div > div"))
    ).text


def get_published_in():
    publishers_element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                             "xpl-document-details > div > "
                                             "div.document-main.global-content-width-w-rr > div > "
                                             "div.document-main-content-container.col-19-24 > section > "
                                             "div.document-main-left-trail-content > div > xpl-document-abstract > "
                                             "section > div.abstract-desktop-div.hide-mobile.text-base-md-lh > "
                                             "div.u-pb-1.stats-document-abstract-publishedIn > a"))
    )
    result = [{"name": publisher.text, "link": publisher.get_attribute('href')} for publisher in publishers_element]
    return result


def get_authors():
    global depth
    try:
        arrow_down = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#authors-header > div > i"))
        )
        arrow_down.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#authors > div"))
        )
        authors_data = driver.find_elements(By.CSS_SELECTOR, "#authors > div")
        result = []
        for author in authors_data:
            author_text = author.text.split('\n')
            if len(author_text) > 1:
                author_info = {
                    "name": author_text[0],
                    "from": author_text[1]
                }
            else:
                author_info = {
                    "name": author.text,
                    "from": None
                }
            result.append(author_info)
        depth += 1
        return result
    except NoSuchElementException:
        return None


def get_ieee_keywords():
    try:
        global depth
        arrow_down = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#keywords-header > div > i"))
        )
        arrow_down.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#keywords > xpl-document-keyword-list > section > div > ul > li:nth-child(1) > ul > li > a"))
        )
        keywords_data = driver.find_elements(By.CSS_SELECTOR,
                                             "#keywords > xpl-document-keyword-list > section > div > ul > li:nth-child("
                                             "1) > ul > li > a")
        result = [keyword.text for keyword in keywords_data]
        depth += 1
        return result
    except NoSuchElementException:
        return None


def get_author_keywords():
    # arrow_down = driver.find_element(By.CSS_SELECTOR, "#keywords-header > div > i")
    # arrow_down.click()
    # time.sleep(1)
    try:
        keywords_data = driver.find_elements(By.CSS_SELECTOR,
                                             "#keywords > xpl-document-keyword-list > section > div > ul > li:nth-child("
                                             "3) > ul > li > a")
        result = [keyword.text for keyword in keywords_data]
        return result
    except NoSuchElementException:
        return None


def determine_type():
    if driver.current_url.__contains__("document"):
        return "Conference Paper"
    else:
        return "irrelevant"


def save_paper(paper):
    global depth
    try:
        paper.click()
    except StaleElementReferenceException:
        # Refetch the paper element if it becomes stale
        papers = get_result_papers()
        paper = papers[papers.index(paper)]
        paper.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "xpl-document-details"))
    )

    type = determine_type()
    paper_data = None
    if type == "Conference Paper":
        paper_data = {
            "Title": get_title(),
            "Pages": get_page(),
            "Cites in Papers": get_cites_papers(),
            "Cites in Patents": get_cites_patents(),
            "Full Text Views": get_full_text_views(),
            "Publisher": get_publisher(),
            "DOI": get_doi(),
            "Date of Publication": get_publication_date(),
            "abstract": get_abstract(),
            "Published in": get_published_in(),
            "Authors": get_authors(),
            "IEEE keywords": get_ieee_keywords(),
            "Author Keywords": get_author_keywords()
        }
        for i in range(0, depth + 1):
            driver.back()
        depth = 0
        return paper_data
    else:
        driver.back()
        return paper_data


def next_page(page):
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, f"stats-Pagination_{str(page + 2)}"))
    )
    button.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, f"stats-Pagination_{str(page + 2)}"))
    )


def scrape(sort_type):
    id = 0
    global depth
    depth = 0
    for page in range(0, 5):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "xpl-results-item"))
        )
        print("currently on page ", page + 1)
        papers = get_result_papers()
        print(papers)
        for paper in papers:
            data = save_paper(paper)
            if data is not None:
                json_data = json.dumps(data)
                with open(f"data1/{sort_type}_{id}.json", "w") as outfile:
                    outfile.write(json_data)
                    print(f"data1/{sort_type}_{id}.json")
                id += 1
        next_page(page)


if __name__ == '__main__':
    search_query = 'Blockchain'
    search_paper(search_query)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "xpl-results-item"))
    )
    handle_cookie_consent()  # Handle cookie consent
    scrape("Relevance")
    drop_down = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#xplMainContent > div.ng-SearchResults.row.g-0 > div.col > "
                                                     "xpl-results-list > div.results-actions.hide-mobile > "
                                                     "xpl-select-dropdown"))
    )
    drop_down.click()
    newest_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#xplMainContent > div.ng-SearchResults.row.g-0 > div.col > "
                                                     "xpl-results-list > div.results-actions.hide-mobile > "
                                                     "xpl-select-dropdown > div > div > button:nth-child(2)"))
    )
    newest_button.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "xpl-results-item"))
    )
    scrape("Newest")
    driver.quit()
