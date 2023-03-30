#coding:utf-8
#接码平台 https://wetalkapp.com/receive-sms-online-usa-12542492894/
#https://sms-activate.org/api2
#https://smsreceivefree.com/
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("detach", True)
driver = webdriver.Chrome( options=options,executable_path=r'C:\Users\Administrator\Desktop\chromedriver_win32\chromedriver.exe')
driver.get('https://poe.com/login')
driver.maximize_window()

input =driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/div[2]/div[1]/form/input')
ActionChains(driver).move_to_element(input).pause(1).click_and_hold().pause(1)\
.send_keys("2542492894").perform()
time.sleep(1)
go=driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/button[1]')
ActionChains(driver).click(go).perform()

time.sleep(3)
code =driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/div[3]/form/input')
ActionChains(driver).move_to_element(code).pause(1).click_and_hold().pause(1)\
.send_keys("973486").perform()

time.sleep(8)
login =driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/button[2]/div')
ActionChains(driver).click(login).perform()

veify =driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/button[2]/div')
ActionChains(driver).click(veify).perform()

text=driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/section/footer/div/div[2]/textarea')
ActionChains(driver).move_to_element(text).pause(1).click_and_hold().pause(1)\
.send_keys("世界上有多少只猴子").perform()

confirm =driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/section/footer/div/div[3]/button/svg')
ActionChains(driver).click(confirm).perform()




# js="window.open('{}','_blank');"
# driver.execute_script(js.format('https://www.supercloudsms.com/en/message/12087444178.html'))
# time.sleep(5)
#driver.execute_script("window.scrollTo(0,document . body. scrollHeight)")