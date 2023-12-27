import json
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from scrapeinlist import insidelist
from selenium.webdriver.chrome.options import Options as ChromeOptions


def scrapesite():
    url = "https://www.olx.pl/elektronika/telefony/smartfony-telefony-komorkowe/q-samsung-s22-ultra/?search%5Border%5D=created_at:desc&search%5Bfilter_float_price:to%5D=2000#842998970"
    #heardersvar = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    olx = 'https://olx.pl'


    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    products = soup.select('div.css-1sw7q4x')

    product_list = []
    temp_id = 'temp_id.txt'
    temp_id_wyrozn = 'temp_id_wyrozn.txt'
    for product in products:
        if product.find('div', class_='css-1jh69qu'):
            id = product.get('id')
            with open(temp_id_wyrozn,'r') as file:
                temp_id_wyrozn_contents = file.read().strip()
            if id in temp_id_wyrozn_contents:
                continue
            else:
                with open(temp_id_wyrozn, 'a') as file:
                    file.write(id + "\n")
                url_class = product.select_one('a', class_='css-rc5s2u')
                combined_url = str(olx + url_class.get('href'))
                item = insidelist(combined_url)
                with open("produktytest.txt", 'w', encoding='utf-8') as file:
                    json.dump(item, file, ensure_ascii=False)
                break

        id = product.get('id')
        with open(temp_id, 'r') as file:
            temp_id_contents = file.read().strip()
        if '"' + id + '"' == temp_id_contents:
            item = None
            break
        else:
            with open (temp_id, 'w') as file:
                json.dump(id, file)
            url_class = product.select_one('a', class_='css-rc5s2u')
            combined_url = str(olx + url_class.get('href'))
            item = insidelist(combined_url)
            with open ("produktytest.txt", 'w', encoding='utf-8') as file:
                json.dump(item, file, ensure_ascii=False)
            break











    return item



