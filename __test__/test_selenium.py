from selenium import webdriver
import time

wd = webdriver.Chrome('E:\\cafe24\\bin\\chromedriver.exe')
wd.get('http://www.google.com')

time.sleep(2)
html = wd.page_source
print(html)

wd.quit()