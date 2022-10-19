import os
import pandas as pd
import requests

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
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    page_source = driver.page_source
    # sleep(60)
    soup = BS(page_source, "html.parser")

    return driver, soup


def create_driver_request(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "x-source": "local",
    }

    response = requests.request("GET", url, headers=headers)

    return response.json()
