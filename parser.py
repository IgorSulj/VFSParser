import time
import credentials
from itertools import cycle
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located, presence_of_element_located, \
    element_to_be_clickable

option_id_by_city = {'Minsk': 'mat-option-0', 'Baranovichi': 'mat-option-1', 'Brest': 'mat-option-2',
                     'Gomel': 'mat-option-3',
                     'Grodno': 'mat-option-4',
                     'Lida': 'mat-option-5', 'Minsk-Premium-Lounge': 'mat-option-6', 'Mogilev': 'mat-option-7',
                     'Pinsk': 'mat-option-8', 'Vitebsk': 'mat-option-9'}


def pass_loading(wait):
    wait.until(visibility_of_element_located((By.CSS_SELECTOR, 'div.ngx-overlay')))
    wait.until_not(visibility_of_element_located((By.CSS_SELECTOR, 'div.ngx-overlay')))


def login():
    options = FirefoxOptions()
    options.headless = True
    driver = Firefox(options=options)
    wait = WebDriverWait(driver, timeout=10000, poll_frequency=0.1)
    driver.get('https://visa.vfsglobal.com/blr/ru/ltu/login')
    wait.until(presence_of_element_located((By.ID, 'mat-input-0')))
    username_field = driver.find_element(By.ID, 'mat-input-0')
    password_field = driver.find_element(By.ID, 'mat-input-1')
    login_button = driver.find_element(By.XPATH,
                                       '/html/body/app-root/div/app-login/section/div/div/mat-card/form/button')
    for i in credentials.email:
        username_field.send_keys(i)
    for i in credentials.password:
        password_field.send_keys(i)
    time.sleep(2)
    wait.until(element_to_be_clickable((By.ID, 'onetrust-button-group-parent')))
    time.sleep(1)
    cookies_button = driver.find_element_by_id('onetrust-button-group-parent')
    cookies_button.click()
    login_button.click()
    return driver, wait


def get_form(driver, wait):
    pass_loading(wait)
    wait.until(element_to_be_clickable((By.XPATH, '/html/body/app-root/div/app-dashboard/section/div/div[2]/button')))
    button = driver.find_element(By.XPATH, '/html/body/app-root/div/app-dashboard/section/div/div[2]/button')
    button.click()


def get_time(driver, wait, city):
    wait.until(element_to_be_clickable((By.ID, "mat-select-0")))
    center_type = driver.find_element(By.ID, "mat-select-0")
    visa_type = driver.find_element(By.ID, 'mat-select-2')
    center_type.click()
    center_id = option_id_by_city[city]
    center = driver.find_element(By.ID, center_id)
    center.click()
    pass_loading(wait)
    visa_type.click()
    wait.until(element_to_be_clickable((By.CSS_SELECTOR, 'mat-option[id^="mat-option-"')))
    long_visa = driver.find_element(By.CSS_SELECTOR, 'mat-option[id^="mat-option-"')
    long_visa.click()
    pass_loading(wait)
    alert = driver.find_elements_by_class_name('alert-info')
    if alert and alert[0].text == 'В настоящее время нет свободных мест для записи':
        return
    # Уведомление
    print('Уведомление')


def main():
    driver, wait = login()
    get_form(driver, wait)
    pass_loading(wait)
    for city in cycle(option_id_by_city.keys()):
        get_time(driver, wait, city)


if __name__ == '__main__':
    main()
