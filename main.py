import random
from termcolor import cprint
from art import text2art
from time import sleep
from rich.console import Console
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from loguru import logger
from config import *


def get_chromedriver():
    options = ChromeOptions() 
    options.add_argument("--disable-blink-features=AutomationControlled") # отключаем режим webdriver
    options.add_argument("--log-level=3") # отключаем вывод логов webdriver
    options.add_extension('Sui Wallet 23.12.12.0.crx')
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(90)
    return driver


def main():
    logger.add('log.log', format="<yellow>{time:YYYY-MM-DD at HH:mm:ss}</yellow> | <level>{level}</level>: <level>{message}</level>")
    logger.info("START")

    driver = get_chromedriver()
    driver.get('chrome-extension://opcgpfmipidbgpenhmajoajpbobppdil/ui.html#/accounts/import-private-key')
    action = ActionChains(driver)
    # ждем пока появится новая страница и закрываем ее
    sleep(1)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    

    input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//textarea[@name="privateKey"]')))
    input.send_keys(PRIVAT_KEY)
    sleep(random.uniform(1,2))
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()


    input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password.input"]')))
    input.send_keys('Svzfdfe34wfdas2312')
    input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password.confirmation"]')))
    input.send_keys('Svzfdfe34wfdas2312')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@id="acceptedTos"]'))).click()
    sleep(random.uniform(1,2))
    input.send_keys(Keys.ENTER)

    sleep(random.uniform(2,3))
    
    driver.get('https://app.suimint.io/mint')

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Connect Wallet"]'))).click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Sui Wallet"]'))).click()
    sleep(random.uniform(1,2))
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Connect"]'))).click()
    sleep(random.uniform(1,2))
    driver.switch_to.window(driver.window_handles[0])

    input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@name="tick"]')))
    input.send_keys(TICK)
    input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@name="amount"]')))
    input.send_keys(AMOUNT)
    input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@name="repeat"]')))
    input.send_keys(Keys.CONTROL + "a")
    input.send_keys(Keys.DELETE)
    input.send_keys(REPEAT)
    sleep(random.uniform(1,2))
    input.send_keys(Keys.ENTER)

    count_approve = 0
    while True:
        try:
            WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
            # sleep(random.uniform(1,2))
            for t in range(MAX_TRIES):
                try:
                    driver.switch_to.window(driver.window_handles[-1])
                    approve = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//button/div[text()="Approve"]')))
                    action.move_to_element(approve).pause(1).move_to_element(approve).click().perform()
                    # sleep(random.uniform(1,2))
                    count_approve+=1
                    logger.success(f'Approve {count_approve}')
                    break
                except:
                    pass
        except:
            if count_approve >= REPEAT:
                break
            # ждем 1-2 минуты для при получении лимита на минт
            try:
                driver.switch_to.window(driver.window_handles[0])
                wait_next = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
                logger.warning(f'Получено ограничение на минт ждем 1 минуту')
                sleep(random.uniform(50,70))
                action.move_to_element(wait_next).pause(1).move_to_element(wait_next).click().perform()
            except:
                pass

    logger.info("FINAL")
    

if __name__ == '__main__':
    console = Console()
    cprint(text2art("SLON", space=1), 'green', end='\n')
    main()
    
