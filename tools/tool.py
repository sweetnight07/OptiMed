
from langchain.tools.base import BaseTool
from utils.cdc_web_scraper import CDCWebScraper
    
class CDCSearchTool(BaseTool):
    name : str = "search_cdc_online"
    description: str = "Searches information about specific health conditions. Input should be the condition name only (e.g., 'diabetes', 'asthma', 'pulmonary embolism')"
    
    def _run(self, query: str) -> str:
        """Execute the CDC search with proper error handling."""
        webscraper = CDCWebScraper()
        try:
            webscraper.update_and_extract_search_url(query)
            webscraper.select_source()
            return webscraper.extract_content_from_source()
        except Exception as e:
            return f"Error searching CDC website: {str(e)}"
        finally:
            webscraper.close()
