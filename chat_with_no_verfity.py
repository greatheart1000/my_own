#coding:utf-8
#接码平台 https://wetalkapp.com/receive-sms-online-usa-12542492894/
#https://sms-activate.org/api2
#https://smsreceivefree.com/
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from lxml import etree
options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("detach", True)
driver = webdriver.Chrome( options=options,
 executable_path=r'C:\Users\Administrator\Desktop\chromedriver_win32\chromedriver.exe')
driver.get('https://poe.com/login')
driver.maximize_window()

input =driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/div[2]/div[1]/form/input')
ActionChains(driver).move_to_element(input).pause(1).click_and_hold().pause(1)\
.send_keys("4807907722").perform()
time.sleep(3)
go=driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/button[1]')
ActionChains(driver).click(go).perform()

time.sleep(3)
code =driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/div[3]/form/input')
ActionChains(driver).move_to_element(code).pause(1).click_and_hold().pause(1)\
.send_keys("259378").perform()
time.sleep(3)
login =driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/button[2]/div')
ActionChains(driver).click(login).perform()

driver.implicitly_wait(3)
coo = driver.get_cookies()
print(coo)
#[{'domain': 'poe.com', 'expiry': 1714961285, 'httpOnly': True, 'name': 'p-b', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'TcpIAfYKGOOHamRIljYfGQ%3D%3D'}]

texts =open('./question.txt','r',encoding='utf-8').readlines()
texts=texts[5000:]
i=0

while i<10000:
    text = driver.find_element(By.XPATH,
                        '//*[@id="__next"]/div[1]/section/footer/div/div[2]/textarea')
    driver.implicitly_wait(3)
    ActionChains(driver).move_to_element(text).pause(1).click_and_hold().pause(1) \
     .send_keys(texts[i]).perform()
    send=driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/section/footer/div/div[3]')
    ActionChains(driver).click(send).perform()
    time.sleep(random.randint(30,40))
    driver.refresh()
    html=driver.page_source
    html =etree.HTML(html)
    texts =html.xpath('//div[@class="Markdown_markdownContainer__UyYrv"]//text()')
    for text in texts:
        text=text.strip().replace(' ','')
        if text:
            print(text)
    i+=1


