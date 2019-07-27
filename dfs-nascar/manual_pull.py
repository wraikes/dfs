import pandas as pd, numpy as np
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path='geckodriver/geckodriver')

tutorial_soup = BeautifulSoup(driver.page_source, 'html.parser')

