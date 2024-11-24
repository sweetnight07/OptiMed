# import other packages 
import os
from dotenv import load_dotenv
from typing import List, Optional

# import langchain packages
from langchain.tools.base import BaseTool

# import utils file
from utils.cdc_web_scraper import CDCWebScraper
from utils.vector_database import PDFVectorDatabase
from utils.ddg_search_engine import DDGSearch

class UserInputTool(BaseTool): # does not need initialization
    name: str = "user_input"
    description: str = "Prompts the user for input and returns their response"

    def _run(self, prompt):
        """
        get input from user with the provided prompt
        """
        return input(f"{prompt}\nYour response: ")

class SearchDatabaseTool(BaseTool): # needs initialization
    name: str = "search_database"
    description: str = "Searchs up relevant information in the vector database."

    def __init__(self, directory_path: str):
        super().__init__()
        self._vector_database: Optional[PDFVectorDatabase] = None
        self._init_database(directory_path)
    
    def _init_database(self, directory_path: str) -> None:
        self._vector_database = PDFVectorDatabase()
        self._vector_database.add_pdf_directory(directory_path)
        self._vector_database.load_pdfs()
        self._vector_database.build_database() 

    def _run(self, query: str):
        """
        runs the query through the vector databases
        """
        documents = self._vector_database.search_with_metadata(query=query)
        content = self._parse_query(documents)
        return content

    def _parse_query(self, documents : List): 
        """
        extracts the content from the output query
        """
        page_contents = [doc.page_content for doc in documents]
        return page_contents

class SearchOnlineTool(BaseTool): # needs initialziation
    name: str = "search_online"
    description: str = "Search online for relevant information regarding the diagnosis."

    def __init__(self):
        super().__init__()
        self._search_engine: Optional[DDGSearch] = None
        self._init_search_engine()
    
    def _init_search_engine(self) -> None:
        self._search_engine = DDGSearch()

    def _run(self, query):
        """
        runs the query through the search engine
        """
        content = self._search_engine.search(query)
        return content
    
class CDCSearchTool(BaseTool):
    name: str = "search_cdc_online"
    description: str = "Searches information about specific health conditions. Input should be the condition name only"
    
    def __init__(self):
        super().__init__()
        self._webscraper: Optional[CDCWebScraper] = None
        self._init_webscraper()
    
    def _init_webscraper(self) -> None:
        self._webscraper = CDCWebScraper()
    
    def _run(self, query: str) -> str:
        if not self._webscraper:
            raise ValueError("Web scraper not initialized")
        try:
            self._webscraper.update_and_extract_search_url(query)
            self._webscraper.select_source()
            return self._webscraper.extract_content_from_source()
        except Exception as e:
            return f"Error searching CDC website: {str(e)}"
        finally:
            if self._webscraper:
                self._webscraper.close()
                self._webscraper = None

