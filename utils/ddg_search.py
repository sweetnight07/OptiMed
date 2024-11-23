from langchain_community.tools import DuckDuckGoSearchRun
from typing import List, Dict, Optional, Union
from datetime import datetime
import logging

class DDGSearch():
    def __init__(self):
        self.search_tool = DuckDuckGoSearchRun()
    
    def search(self, query: str):
        try:
            return self.search_tool.invoke(query)
        except Exception as e:
            print(f"Invalid Search: {str(e)}")
            return None