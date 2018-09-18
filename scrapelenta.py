from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import os
import time

# TODO: Add location parsing

def clear():
    os.system('cls')


def add_shop(stype):
    if int(stype) == 1:
        return ' (гипермаркет)'
    else:
        return ' (супермаркет)'


def get_link_text(f_link):
    linktext = f_link.get_attribute("href")
    a = linktext.find('http')
    b = linktext.rfind("'")
    return linktext[a:b]


# TODO: Add parsing city list from the site instead of a file
# TODO: Write into .JSON fine instead of .txt
file = open('lentascrape.txt', 'a')
citylist = open('citylist.txt', 'r')
cities = []

with open('citylist.txt') as openfileobject:
    for line in openfileobject:
        cities.append(line[:-1])

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('http://www.lenta.com')

cityCount = 1
for cityName in cities:
    print(f'{cityCount}. {cityName}')
    file.write(f'{cityCount}. {cityName}' + '\n')
    city = driver.find_element_by_link_text(cityName)
    city.click()
    time.sleep(2)
    try:
        catalogue = driver.find_element_by_link_text('Гипермаркеты')
        catalogue.click()
    except NoSuchElementException:
        catalogue = driver.find_element_by_link_text('Магазины')
        catalogue.click()
    time.sleep(4)
    table = driver.find_elements_by_tag_name('table')

    # Проверка на наличие легенды с точками. Если в массиве два значения, города - во второй таблице
    # TODO: Rework shop type parsing (from <a> instead of <div>)
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
        file.write(line + '\n')
    catalogue = driver.find_element_by_link_text('Электронный каталог')
    catalogue.click()
    cLinks = driver.find_elements_by_partial_link_text('25 лет')

    # TODO: Make Moscow district cities to get a supermarket link

    # Проверка на количество ссылок на каталоги. Если 1, то там только гиперы
    n = 1
    if len(cLinks) > 1:
        for link in cLinks:
            linkText = get_link_text(link)
            if n == 1:
                print(f'Каталог супермаркета: {linkText}')
                file.write(f'Каталог супермаркета: {linkText}' + '\n')
            else:
                print(f'Каталог гипермаркета: {linkText}')
                file.write(f'Каталог гипермаркета: {linkText}' + '\n')
            n += 1
    else:
        linkText = get_link_text(cLinks[0])
        print(f'Каталог гипермаркета: {linkText}')
        file.write(f'Каталог гипермаркета: {linkText}' + '\n')

    file.write('\n')
    cityCount += 1
    select_city = driver.find_element_by_id('topCityName')
    select_city.click()
    time.sleep(2)

citylist.close()
file.close()
driver.quit()
