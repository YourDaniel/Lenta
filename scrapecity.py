from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import os
import time


def clear():
    os.system('cls')


def add_shop(stype):
    if int(stype) == 1:
        return ' (гипермаркет)'
    else:
        return ' (супермаркет)'


def get_link_text(f_link):
    linkText = f_link.get_attribute("href")
    a = linkText.find('http')
    b = linkText.rfind("'")
    return linkText[a:b]


driver = webdriver.Chrome()
driver.maximize_window()
driver.get('http://www.lenta.com')

cityName = 'Альметьевск'
print(f'Test City. {cityName}')
city = driver.find_element_by_link_text(cityName)
city.click()
time.sleep(2)

try:
    catalogue = driver.find_element_by_link_text('Гипермаркеты')
    print(catalogue.get_attribute('href'))
    catalogue.click()
except NoSuchElementException:
    catalogue = driver.find_element_by_link_text('Магазины')
    print(catalogue.get_attribute('href'))
    catalogue.click()


table = driver.find_elements_by_tag_name('table')
if len(table) == 0:
    catalogue = driver.find_element_by_link_text('Гипермаркеты')
    catalogue.click()
    table = driver.find_elements_by_tag_name('table')

if len(table) > 1:
    dots = table[1].find_elements_by_tag_name('div')
else:
    dots = table[0].find_elements_by_tag_name('div')
for i in dots:
    link = i.find_element_by_tag_name('a')
    shopType = i.get_attribute('class')
    a = shopType.find('type')
    shopType = shopType[a + 5]
    line = link.text + add_shop(shopType)
    print(line)

catalogue = driver.find_element_by_link_text('Электронный каталог')
catalogue.click()
cLinks = driver.find_elements_by_partial_link_text('25 лет')
n = 1
if len(cLinks) > 1:
    for link in cLinks:
        linkText = get_link_text(link)
        if n == 1:
            print(f'Каталог супермаркета: {linkText}')
        else:
            print(f'Каталог гипермаркета: {linkText}')
        n += 1
else:
    linkText = get_link_text(cLinks[0])
    print(f'Каталог гипермаркета: {linkText}')
time.sleep(5)
driver.quit()
