# selenium 4
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

option = webdriver.ChromeOptions()
# option.add_argument("start-maximized")
option.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.get('https://ieeexplore.ieee.org/Xplore/home.jsp')


# searching for paper
def search_paper(query):
    search_box = driver.find_element(By.TAG_NAME, 'input')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)


def get_result_papers():
    return driver.find_elements(By.CSS_SELECTOR,
                                'xpl-results-item > div.hide-mobile > div.d-flex.result-item > div.col.result-item-align.px-3 > h3 > a')


def has_page_number():
    return False


def get_title():
    title = driver.find_element(By.CSS_SELECTOR,
                                "xpl-document-details > div > div.document-main.global-content-width-w-rr > "
                                "section.document-main-header.row.g-0 > div > xpl-document-header > section > "
                                "div.document-header-inner-container.row.g-0 > div > div > "
                                "div.row.g-0.document-title-fix > div > div.left-container.w-100 > h1 > span")
    return title.text


def get_cites_papers():
    num_cites = driver.find_element(By.CSS_SELECTOR,
                                    "xpl-document-details > div > div.document-main.global-content-width-w-rr > "
                                    "section.document-main-header.row.g-0 > div > xpl-document-header > section > "
                                    "div.document-header-inner-container.row.g-0 > div > div > "
                                    "div.document-main-subheader > "
                                    "div.document-header-metrics-banner.d-flex.flex-wrap > "
                                    "div.document-banner.col.stats-document-banner > "
                                    "div.document-banner-metric-container.d-flex > button:nth-child(1) > "
                                    "div.document-banner-metric-count").text
    return int(num_cites)


# returns zero if the paper has no cites in patent
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
    try:
        views = driver.find_element(By.CSS_SELECTOR,
                                    "xpl-document-details > div > div.document-main.global-content-width-w-rr > "
                                    "section.document-main-header.row.g-0 > div > xpl-document-header > section > "
                                    "div.document-header-inner-container.row.g-0 > div > div > "
                                    "div.document-main-subheader > "
                                    "div.document-header-metrics-banner.d-flex.flex-wrap > "
                                    "div.document-banner.col.stats-document-banner > "
                                    "div.document-banner-metric-container.d-flex > button:nth-child(3) > "
                                    "div.document-banner-metric-count").text
    except NoSuchElementException:
        views = driver.find_element(By.CSS_SELECTOR,
                                    "xpl-document-details > div > div.document-main.global-content-width-w-rr > "
                                    "section.document-main-header.row.g-0 > div > xpl-document-header > section > "
                                    "div.document-header-inner-container.row.g-0 > div > div > "
                                    "div.document-main-subheader > "
                                    "div.document-header-metrics-banner.d-flex.flex-wrap > "
                                    "div.document-banner.col.stats-document-banner > "
                                    "div.document-banner-metric-container.d-flex > button:nth-child(2) > "
                                    "div.document-banner-metric-count").text
    return int(views)


def get_publisher():
    publisher = driver.find_element(By.CSS_SELECTOR, "xpl-document-details > div > "
                                                     "div.document-main.global-content-width-w-rr > div > "
                                                     "div.document-main-content-container.col-19-24 > section > "
                                                     "div.document-main-left-trail-content > div > "
                                                     "xpl-document-abstract > section > "
                                                     "div.abstract-desktop-div.hide-mobile.text-base-md-lh > "
                                                     "div.row.g-0.u-pt-1 > div:nth-child(2) > "
                                                     "div.u-pb-1.doc-abstract-publisher > xpl-publisher > span > span "
                                                     "> span > span:nth-child(2)").text
    return publisher


def get_doi():
    doi = driver.find_element(By.CSS_SELECTOR, "xpl-document-details > div > "
                                               "div.document-main.global-content-width-w-rr > div > "
                                               "div.document-main-content-container.col-19-24 > section > "
                                               "div.document-main-left-trail-content > div > xpl-document-abstract > "
                                               "section > div.abstract-desktop-div.hide-mobile.text-base-md-lh > "
                                               "div.row.g-0.u-pt-1 > div:nth-child(2) > "
                                               "div.u-pb-1.stats-document-abstract-doi > a").text
    return doi


def get_publication_date():
    publication_date = driver.find_element(By.CSS_SELECTOR, 'xpl-document-details > '
                                                            'div > div.document-main.global-content-width-w-rr > div '
                                                            '> div.document-main-content-container.col-19-24 > '
                                                            'section > div.document-main-left-trail-content > div > '
                                                            'xpl-document-abstract > section > '
                                                            'div.abstract-desktop-div.hide-mobile.text-base-md-lh > '
                                                            'div.row.g-0.u-pt-1 > div:nth-child(1) > '
                                                            'div.u-pb-1.doc-abstract-confdate').text
    return publication_date.split(': ')[1]


def get_abstract():
    return driver.find_element(By.CSS_SELECTOR, "xpl-document-details > div > "
                                                "div.document-main.global-content-width-w-rr > div > "
                                                "div.document-main-content-container.col-19-24 > section > "
                                                "div.document-main-left-trail-content > div > xpl-document-abstract > "
                                                "section > div.abstract-desktop-div.hide-mobile.text-base-md-lh > "
                                                "div.abstract-text.row.g-0 > div > div > div").text


def get_published_in():
    publishers_element = driver.find_elements(By.CSS_SELECTOR,
                                              "xpl-document-details > div > "
                                              "div.document-main.global-content-width-w-rr > div > "
                                              "div.document-main-content-container.col-19-24 > section > "
                                              "div.document-main-left-trail-content > div > xpl-document-abstract > "
                                              "section > div.abstract-desktop-div.hide-mobile.text-base-md-lh > "
                                              "div.u-pb-1.stats-document-abstract-publishedIn > a")
    result = [{"name": publisher.text, "link": publisher.get_attribute('href')} for publisher in publishers_element]
    return result


def get_authors():
    arrow_down = driver.find_element(By.CSS_SELECTOR, "#authors-header > div > i")
    arrow_down.click()
    time.sleep(1)
    authors_data = driver.find_elements(By.CSS_SELECTOR, "#authors > div")
    result = [{"name": author.text.split('\n')[0], "from": author.text.split('\n')[1]} for author in authors_data]
    # print(authors_data.pop().text)
    return result


def save_paper(paper):
    paper.click()
    time.sleep(2)
    paper_data = {
        "Title": get_title(),
        "Pages": None,
        "Cites in Papers": get_cites_papers(),
        "Cites in Patents": get_cites_patents(),
        "Full Text Views": get_full_text_views(),
        "Publisher": get_publisher(),
        "DOI": get_doi(),
        "Date of Publication": get_publication_date(),
        "abstract": get_abstract(),
        "Published in": get_published_in(),
        "Authors": get_authors(),

    }
    return paper_data


def next_page():
    return


if __name__ == '__main__':
    search_paper('Blockchain')
    time.sleep(5)
    # for page in range(0, 5):
    papers = get_result_papers()
    print(papers)
    # for paper in papers:
    data = save_paper(papers.pop())
    print(data)

    driver.quit()
