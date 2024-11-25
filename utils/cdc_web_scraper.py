# import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException



class CDCWebScraper:
    def __init__(self):
        """
        initialize the webscraper database
        """
        self.base_url = "https://www.cdc.gov/health-topics.html"
        self.driver = self.setup_driver()
        self.result_url = None # the queried result url
        self.first_result_link = None # the first link

    def setup_driver(self):
        """
        sets up the driver once
        """
        # Setup Selenium WebDriver with headless mode
        options = Options()
        options.add_argument('--headless')  # configuration
        options.add_argument('--disable-gpu') 
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')

        # emulate on a chrome browser
        driver = webdriver.Chrome(options=options)
        return driver

    def update_and_extract_search_url(self, query: str):
        """
        updates the search url whenever there is a new query
        """
        # load the base url
        try:
            # load the base url
            self.driver.get(self.base_url)

            # find and fill in the search bar
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="cdc-atozsearch"]//input[@placeholder="Search Health Topics"]'))
            )
            search_input.send_keys(query)

            # click the search button
            search_button = self.driver.find_element(By.ID, "az-search-submit")
            search_button.click()

            # wait for the results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "results"))
            )

            self.result_url = self.driver.current_url

            return self.result_url
        
        except TimeoutException:
            return "Search page took too long to load"
        except NoSuchElementException as e:
            return f"Element not found: {e}"
        except Exception as e:
            return f"Error during search: {e}"

    def select_source(self):
        """
        selects the first link
        """
        try:
            if not self.result_url:
                raise KeyError("no result page to choose from, please extract first")
            
            # navigate to the result page
            self.driver.get(self.result_url)

            # wait for the first result link to appear
            first_result = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '(//div[@class="result-title d-flex"]//a)[1]'))
            )

            # optimization like page rank or llm judges the best href
            self.first_result_link = first_result.get_attribute('href')
            return self.first_result_link
        except TimeoutException:
            return "Search result page took too long to load"
        except NoSuchElementException as e:
            return f"First result link not found: {e}"
        except Exception as e:
            return f"Error selecting source: {e}"
    
    def extract_content_from_source(self):
        """
        extract all of the textual content from the self.first_result_link
        """
        print(f"extracting content from: {self.first_result_link}")
        
        # prevent errors
        if not self.first_result_link:
            return "no information - link is empty"
        
        try:
            # navigate to the url
            self.driver.get(self.first_result_link)

            # wait for the page to fully load (e.g., wait until <body> tag is present)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

        except Exception as e:
            print(f"error navigating to the page or waiting for load: {e}")
            return "error navigating to the page"

        try:
            # tags to extract content from
            tags_to_extract = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "span"]
            content = []

            for tag in tags_to_extract:
                # check if elements for the current tag exist
                elements = self.driver.find_elements("tag name", tag)
                
                # silently skip if no elements are found
                if not elements:
                    continue
                
                # extract and add text content from elements
                # optimize it by having an structures
                tag_content = [e.text for e in elements if e.text.strip()]
                content.extend(tag_content)

            # combine all extracted content
            full_content = "\n".join(content).strip()

            # check if there's meaningful content
            if not full_content:
                return "no relevant content found in the specified tags"

            return full_content

        # error catch
        except Exception as e:
            print(f"an error occurred while extracting content: {e}")
            return "error extracting content"

    # closes the webscraper
    def close(self): 
        self.driver.quit()
        



