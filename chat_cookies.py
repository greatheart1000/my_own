import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json
import random
from lxml import etree
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('User-Agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                     ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
options.add_experimental_option("excludeSwitches", ["enable-automation"]) #去除收到自动化测试的特征
options.add_argument("disable-blink-features=AutomationControlled")
options.add_experimental_option("useAutomationExtension",False)
options.add_experimental_option("detach", True)

driver=webdriver.Chrome(options=options,
    executable_path=r'C:\Users\Administrator\Desktop\chromedriver_win32\chromedriver.exe')
driver.get('https://poe.com/login')
driver.implicitly_wait(3)
driver.maximize_window()

cookies=  [{'domain': 'poe.com', 'expiry': 1714961285, 'httpOnly': True, 'name': 'p-b', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'TcpIAfYKGOOHamRIljYfGQ%3D%3D'}]

for cookie in cookies:
    if "expiry" in cookies:
        del cookie['expiry']
    driver.add_cookie(cookie)
driver.refresh()
driver.get('https://poe.com/login')
time.sleep(8)
chatGPT = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/aside/div/div/section[1]/a[5]')
ActionChains(driver).click(chatGPT).perform()

questions =open('./question.txt','r',encoding='utf-8').readlines()
qs=questions[4390:]
i=0
f=open('./corpus.txt','a',encoding='utf-8')

while i<10000:

    text = driver.find_element(By.XPATH,
                        '//*[@id="__next"]/div[1]/section/footer/div/div[2]/textarea')
    driver.implicitly_wait(3)
    ActionChains(driver).move_to_element(text).pause(1).click_and_hold().pause(1) \
     .send_keys(qs[i]).perform()
    send=driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/section/footer/div/div[3]')
    ActionChains(driver).click(send).perform()
    time.sleep(random.randint(25,35))
    driver.refresh()
    html=driver.page_source
    html =etree.HTML(html)
    texts =html.xpath('//div//div[@class="ChatMessage_messageRow__7yIr2"]//text()')
    questions =html.xpath('////div[@class="Message_botMessageBubble__CPGMI"]//text()')
    for text in texts:
        text = text.strip().replace(' ', '')
        if text:
            # print(text)
            f.write(str(text)+'\n')
    i+=1
    if i%20==0:
        print(i)
    if i==1000:
        break
f.close()


# text=driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/section/footer/div/div[2]/textarea')
# driver.implicitly_wait(3)
# ActionChains(driver).move_to_element(text).pause(1).click_and_hold().pause(1)\
# .send_keys("世界上有多少只猴子").perform()


# input =driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/div[2]/div[1]/form/input')
# ActionChains(driver).move_to_element(input).pause(1).click_and_hold().pause(1)\
# .send_keys("8254621258").perform()
# time.sleep(3)
# go=driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/button[1]')
# ActionChains(driver).click(go).perform()

"""
[{'domain': 'poe.com', 'expiry': 1714995166, 'httpOnly': True, 'name': 'p-b', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'xik2Yc65qoKwuw-i3hXg2g%3D%3D'}]
[{'domain': 'poe.com', 'expiry': 1714995629, 'httpOnly': True, 'name': 'p-b', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '0oclmKfSmfT9mQc0uru1GQ%3D%3D'}]
[{'domain': 'poe.com', 'expiry': 1714995779, 'httpOnly': True, 'name': 'p-b', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'bE5QTyOC4tYpS-U7tZmVXA%3D%3D'}]
[{'domain': 'poe.com', 'expiry': 1714995866, 'httpOnly': True, 'name': 'p-b', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'c5rrxtu7c9pcF3ZFgmDfnQ%3D%3D'}]
[{'domain': 'poe.com', 'expiry': 1714996206, 'httpOnly': True, 'name': 'p-b', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 't5NZqW-gnXM9CNwVKjQqFA%3D%3D'}]


"""







