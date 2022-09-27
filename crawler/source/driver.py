import os
import pandas as pd

from bs4 import BeautifulSoup as BS

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

from .constant import URL_PRODUCT
from .tables import BRANDS, PRODUCTS
from .utils import pre_tag_to_json, json_dump

from time import sleep

BASE_DIR = os.getcwd()


def create_driver(url):

    chromedriver_path = os.path.join(BASE_DIR, "source", "chromedriver_105.exe")

    service = ChromeService(executable_path=chromedriver_path)

    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--headless")
    options.set_capability("x-source", "local")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    page_source = driver.page_source
    # sleep(60)
    soup = BS(page_source, "html.parser")

    return driver, soup


def product_crawl(url):
    driver, page = create_driver(url)

    products = pre_tag_to_json(page)["data"]

    return products


def product_crawl2(url):
    driver, page = create_driver(url)

    products = pre_tag_to_json(page)["data"]

    total_products = len(products)

    for i in range(total_products):
        product = products[0]
        # seller_row = []
        # product_row = []
        # product_detail_row = []

        # json_dump(product)

        brand_row = dict((key, product[BRANDS[key]]) for key in BRANDS)

        url_product = f"{URL_PRODUCT}/{product['id']}"
        driver_product, page_product = create_driver(url_product)

        product_page_data = pre_tag_to_json(page_product)

        product_1 = dict((key, product[BRANDS[key]]) for key in PRODUCTS)

        print(product_page_data["master_id"])

        driver_product.close()
        # product_row = dict((key, product[PRODUCTS[key]]) for key in PRODUCTS)

        # print(brand_row)
        break

    # Close
    driver.close()

    return brand_row
