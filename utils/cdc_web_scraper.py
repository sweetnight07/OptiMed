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
        self.base_url = "https://www.cdc.gov/health-topics.html"
        self.driver = self.setup_driver()
        self.result_url = None # the queried result url
        self.first_result_link = None # the first link

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

    def update_and_extract_search_url(self, query: str):
        # load the base uril
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
        try:
            if not self.result_url:
                raise KeyError("no result page to choose from, please extract first")
            
            # navigate to the result page
            self.driver.get(self.result_url)

            # wait for the first result link to appear
            first_result = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '(//div[@class="result-title d-flex"]//a)[1]'))
            )
            self.first_result_link = first_result.get_attribute('href')

            return self.first_result_link
        except TimeoutException:
            return "Search result page took too long to load"
        except NoSuchElementException as e:
            return f"First result link not found: {e}"
        except Exception as e:
            return f"Error selecting source: {e}"
    

    def extract_content_from_source(self):
        print(self.first_result_link)
        content = ""

        if not self.first_result_link:
            return "No Information"
        
        try: 
            self.driver.get(self.first_result_link)

            # wait for the content to load
            body_div = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cdc-dfe-body"))
            )

            found_section = False
            sections = body_div.find_elements(By.CLASS_NAME, "dfe-section")

            if not sections:
                return "No Information"
            for section in sections:
                # extract the section's title (h2 or h3) if available
                heading = ""
                headings = section.find_elements(By.XPATH, "./h2 | ./h3")
                if headings: 
                    heading = headings[0].text
                else:
                    heading = "No heading found"  
            
                content += f"\n{heading}\n"
                
                found_section = True

                # extract paragraphs in the section if any are found
                paragraphs = section.find_elements(By.TAG_NAME, "p")
                if paragraphs:
                    for para in paragraphs:
                        content += f"{para.text}\n\n"
                else:
                    content += "No paragraphs found.\n\n"  # handle case where no paragraphs exist

                # extract list items in the section if any are found
                list_items = section.find_elements(By.TAG_NAME, "li")
                if list_items:
                    for li in list_items:
                        content += f"- {li.text}\n"
                else:
                    content += "No list items found.\n"  # handle case where no list items exist
                
                if not found_section:
                    return "No Information"
        except NoSuchElementException as e:
            return "No Information"
        except TimeoutException:
            return "Content took too long to load"
        except Exception as e:
            return f"Error extracting content: {e}"
        
        return content

    def close(self): 
        self.driver.quit()
        



