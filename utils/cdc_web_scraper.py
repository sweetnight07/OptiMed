from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CDCWebScraper:
    def __init__(self):
        self.base_url = "https://www.cdc.gov/health-topics.html"
        self.driver = self.setup_driver()
        self.search_box = None

    def setup_driver(self):
        # Setup Selenium WebDriver with headless mode
        options = Options()
        options.add_argument('--headless')  # configuration
        options.add_argument('--disable-gpu') 
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')

        driver = webdriver.Chrome(options=options)
        return driver

    def extract_search_url(self, query: str):
        # load the base uril
        self.driver.get(self.base_url)

        # fill in the search bar
        search_input = self.driver.find_element(By.XPATH, '//div[@id="cdc-atozsearch"]//input[@placeholder="Search Health Topics"]')

        # insert keys which adds to values
        search_input.send_keys(query)

        # once filled you can press search 
        search_button = self.driver.find_element(By.ID, "az-search-submit")
        search_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "results"))
        )

        self.url = self.driver.current_url

        return self.url

    def select_information():

        return None

    def close(self): 
        self.driver.quit()



