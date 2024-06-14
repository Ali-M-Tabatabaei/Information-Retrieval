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
                                'xpl-results-item > div.hide-mobile > div.d-flex.result-item > '
                                'div.col.result-item-align.px-3 > h3 > a')


def has_page_number():
    return False


def get_title():
    title = driver.find_element(By.CSS_SELECTOR,
                                "xpl-document-details > div > div.document-main.global-content-width-w-rr > "
                                "section.document-main-header.row.g-0 > div > xpl-document-header > section > "
                                "div.document-header-inner-container.row.g-0 > div > div > "
                                "div.row.g-0.document-title-fix > div > div.left-container.w-100 > h1 > span")
    # except NoSuchElementException:
    #     title = driver.find_element(By.CSS_SELECTOR, "xpl-courses > div > xpl-courses-details > div > "
    #                                                  "div.header--course-details.row.g-0.global-margins > "
    #                                                  "div.col.header--course-details__title-icon-container.u-flex"
    #                                                  "-display-flex.u-flex-align-items-center > "
    #                                                  "div.col.header--course-details__title-container > h2")
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
    views = 0
    buttons = driver.find_elements(By.CSS_SELECTOR,
                                   "xpl-document-details > div > div.document-main.global-content-width-w-rr > "
                                   "section.document-main-header.row.g-0 > div > xpl-document-header > section > "
                                   "div.document-header-inner-container.row.g-0 > div > div > "
                                   "div.document-main-subheader > "
                                   "div.document-header-metrics-banner.d-flex.flex-wrap > "
                                   "div.document-banner.col.stats-document-banner > "
                                   "div.document-banner-metric-container.d-flex > button")
    for button in buttons:
        if button.text.__contains__("Views"):
            views = int(button.text.split('\n')[0])
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


# "#xplMainContentLandmark > div > xpl-document-details > div > div.document-main.global-content-width-w-rr > div > div.document-main-content-container.col-19-24 > section > div.document-main-left-trail-content > div > xpl-document-abstract > section > div.abstract-desktop-div.hide-mobile.text-base-md-lh > div.row.g-0.u-pt-1 > div:nth-child(1) > div.u-pb-1.doc-abstract-pubdate"
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
        publication_date = driver.find_element(By.CSS_SELECTOR, 'xpl-document-details '
                                                                '> div > div.document-main.global-content-width-w-rr '
                                                                '> div > '
                                                                'div.document-main-content-container.col-19-24 > '
                                                                'section > div.document-main-left-trail-content > div '
                                                                '> xpl-document-abstract > section > '
                                                                'div.abstract-desktop-div.hide-mobile.text-base-md-lh '
                                                                '> div.row.g-0.u-pt-1 > div:nth-child(1) > '
                                                                'div.u-pb-1.doc-abstract-pubdate').text

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


def get_ieee_keywords():
    arrow_down = driver.find_element(By.CSS_SELECTOR, "#keywords-header > div > i")
    arrow_down.click()
    time.sleep(1)
    keywords_data = driver.find_elements(By.CSS_SELECTOR,
                                         "#keywords > xpl-document-keyword-list > section > div > ul > li:nth-child(1) > ul > li > a")
    result = [keyword.text for keyword in keywords_data]
    return result


def get_author_keywords():
    # arrow_down = driver.find_element(By.CSS_SELECTOR, "#keywords-header > div > i")
    # arrow_down.click()
    # time.sleep(1)
    keywords_data = driver.find_elements(By.CSS_SELECTOR,
                                         "#keywords > xpl-document-keyword-list > section > div > ul > li:nth-child("
                                         "3) > ul > li > a")
    result = [keyword.text for keyword in keywords_data]
    return result


def determine_type():
    if driver.current_url.__contains__("document"):
        return "Conference Paper"
    else:
        return "irrelevant"


def save_paper(paper):
    paper.click()
    time.sleep(2)
    type = determine_type()
    paper_data = None
    if type == "Conference Paper":
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
            "IEEE keywords": get_ieee_keywords(),
            "Author Keywords": get_author_keywords()
        }
        driver.back()
        driver.back()
        driver.back()
        return paper_data
    else:
        driver.back()
        return paper_data


def next_page(page):
    button = driver.find_element(By.CLASS_NAME, f"stats-Pagination_{str(page + 2)}")
    button.click()
    time.sleep(1)


if __name__ == '__main__':
    search_query = 'Blockchain'
    search_paper(search_query)
    time.sleep(5)
    for page in range(0, 5):
        time.sleep(5)
        print("currently on page ", page + 1)
        papers = get_result_papers()
        print(papers)
        for paper in papers:
            data = save_paper(paper)
            print(data)
            time.sleep(3)
        print(driver.current_url)
        next_page(page)

    driver.quit()
