import time
from selenium import webdriver


browsr = webdriver.Chrome("/Users/Jawad/Desktop/Automation/chromedriver.exe")
browsr.get('https://www.instagram.com/accounts/login/?source=auth_switcher')