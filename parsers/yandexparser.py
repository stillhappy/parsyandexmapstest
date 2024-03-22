from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import random

def infinite_scroll(driver):
    number_of_elements_found = 0
    while True:
        els = driver.find_elements(By.CSS_SELECTOR, '.search-snippet-view')
        if number_of_elements_found == len(els):
            # Reached the end of loadable elements
            break

        try:
            driver.execute_script("arguments[0].scrollIntoView();", els[-1])
            number_of_elements_found = len(els)

        except:
            # Possible to get a StaleElementReferenceException. Ignore it and retry.
            pass
        time.sleep(1)

def YandexPars(city, category):
    proxies = ['138.124.186.18:8000', '193.9.17.244:8000', '45.145.160.130:8000']
    ua = UserAgent()
    user_agent = ua.random

    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument(f"--proxy-server={proxies[0]}")
    # chrome_options.add_argument(f"--proxy-server={proxies[1]}")
    # chrome_options.add_argument(f"--proxy-server={proxies[2]}")
    # chrome_options.add_argument(f"--user-agent={user_agent}")

    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get('https://yandex.ru/maps/')
        time.sleep(random.uniform(1, 3))
        txt = driver.find_element(By.CLASS_NAME, 'input__control._bold')
        txt.send_keys(f'{city}, {category}')
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'small-search-form-view__button')))
        button.click()
        time.sleep(random.uniform(2, 4))
        driver.refresh()
        time.sleep(random.uniform(1, 3))
        infinite_scroll(driver)
        driver.maximize_window()
        now = datetime.now()
        current_time = now.strftime('%Y-%m-%d %H:%M')
        # Дата, Баз, оп, Город, Сфера, Название, площадка, тип_клиента, ссылка на карточку, кол-во отзывов, рейтинг, ссылка на сайт, Телефон, Результат, дата звонка, email, оплата1, оплата2
        buts = driver.find_elements(By.CLASS_NAME, 'search-business-snippet-view__title')
        list_orgs = []
        for but in buts:
            try:
                driver.execute_script("arguments[0].click();", but)
                time.sleep(random.uniform(1, 3))
                url_card = f'https://yandex.ru/maps/org/{driver.find_element(By.CLASS_NAME, 'business-card-view').get_attribute('data-id')}/'
                name = driver.find_element(By.CLASS_NAME, 'card-title-view__title-link').text
                rating = driver.find_element(By.CLASS_NAME, 'business-rating-badge-view__rating-text').text
                count_s = driver.find_element(By.CLASS_NAME, 'business-header-rating-view__text._clickable').text
                url_site_element = driver.find_elements(By.CLASS_NAME, 'action-button-view._type_web')
                url_site = url_site_element[0].find_element(By.TAG_NAME, 'a').get_attribute(
                    'href') if url_site_element else 'Нет'
                try:
                    phone_element = driver.find_element(By.CLASS_NAME, 'card-phones-view__number')
                    phone = phone_element.text
                    # Добавьте здесь код для обработки найденного телефонного номера
                except NoSuchElementException:
                    # Обработка случая, когда элемент не найден
                    phone = "Номер телефона не указан"
                l_org = [current_time, name, city, category, 'ЯндексКарты', 'L', 'L', url_card, rating, count_s,
                         url_site, phone]
                list_orgs.append(l_org)
                time.sleep(random.uniform(2, 4))
            except: # для начала
                continue
    return list_orgs


if __name__ == '__main__':
    city = 'Видное'
    category = 'Аптеки'
    YandexPars(city, category)