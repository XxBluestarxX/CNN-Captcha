from selenium import webdriver
from lxml import etree 
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
import time
base_url = 'https://tixcraft.com'
url = 'https://tixcraft.com/ticket/ticket/26_ffotp/22467/1/16'
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.get(url)
input()
for i in range(10):
    try:
        captha_img = driver.find_element(By.ID, 'TicketForm_verifyCode-image')
        captha_img.screenshot(f'.\\test_captcha\\captcha_{i}.png')
        print(f'save {i} captcha')
        captha_img.click()
        time.sleep(2)
    except:
        input()