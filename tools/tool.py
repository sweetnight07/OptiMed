# import other packages 
from typing import List, Optional
from datetime import datetime
import re
import ast

# import langchain packages
from langchain.tools.base import BaseTool

# import utils file
from utils.cdc_web_scraper import CDCWebScraper
from utils.vector_database import PDFVectorDatabase
from utils.ddg_search_engine import DDGSearch
from utils.google_calendar import GoogleCalendarAPI

class RespondTool(BaseTool):
    name: str= "respond_tool"
    description: str = ""
    def _run(self, input: str) -> str:
        """
        generates a response to the given input.
        """
        # 
        return f"Response: {input}"
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
        """
        init that wraps the tool as a BaseTool and initializes the actual tool
        """
        super().__init__()
        self._vector_database: Optional[PDFVectorDatabase] = None
        self._init_database(directory_path)
    
    def _init_database(self, directory_path: str) -> None:
        """
        initializes the database as a tool
        """
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
        """
        init that wraps the tool as a BaseTool and initializes the actual tool
        """
        super().__init__()
        self._search_engine: Optional[DDGSearch] = None
        self._init_search_engine()
    
    def _init_search_engine(self) -> None:
        """
        initializes the duckduck go as a tool
        """
        self._search_engine = DDGSearch()

    def _run(self, query):
        """
        runs the query through the search engine
        """
        content = self._search_engine.search(query)
        return content
    
class CDCSearchTool(BaseTool): # needs initialization
    name: str = "search_cdc_online"
    description: str = "Searches information about specific health conditions. Input should be the condition name only"
    
    def __init__(self):
        """
        init that wraps the tool as a BaseTool and initializes the actual tool
        """
        super().__init__()
        self._webscraper: Optional[CDCWebScraper] = None
        self._init_webscraper()
    
    def _init_webscraper(self) -> None:
        """initializes the webscraper as a tool
        """
        self._webscraper = CDCWebScraper()
    
    def _run(self, query: str) -> str:
        """
        runs the webscraper
        """
        if not self._webscraper:
            raise ValueError("Web scraper not initialized")
        try:
            self._webscraper.update_and_extract_search_url(query)
            self._webscraper.select_source()
            return self._webscraper.extract_content_from_source()
        except Exception as e:
            return f"Error searching CDC website: {str(e)}"
        
class ParseAppointmentTool(BaseTool): # does not need initialization
    name: str = "parse_appointment"
    description: str = "parses the 'appointment_details' into a formatted output so it can be schedule"
    
    def _run(self, appointment_details: str):
        """
        runs the parser
        """
        # clean
        appointment_details = re.sub(r'[^0-9/:,\- ]', '', appointment_details).strip()
        
        # pplit into date and time parts
        date_part, time_part = appointment_details.split(", ")
        start_time_str, end_time_str = [t.strip() for t in time_part.split("-")]
        
        # parse date components
        month, day, year = map(int, date_part.split("/"))
        
        # parse start time
        start_hour, start_minute = map(int, start_time_str.split(":"))
        
        # parse end time
        end_hour, end_minute = map(int, end_time_str.split(":"))
        
        return {
            'summary': '', 
            'description': '',  
            'year': year,
            'month': month,
            'day': day,
            'start_hour': start_hour,
            'start_minute': start_minute,
            'end_hour': end_hour,
            'end_minute': end_minute
        }

class ScheduleAppointmentTool(BaseTool): # needs initialization
    name: str = "schedule_appointment"
    description: str = "Passes in the output of the parsed tool, and the start and  and fill in neccessary description and schedules an appointment into the google calendar"

    def __init__(self):
        """
        init that wraps the tool as a BaseTool and initializes the actual tool
        """
        super().__init__()
        self._calendar_api = None
        self._init_calendar()
    
    def _init_calendar(self) -> None:
        """
        initialize the Google Calendar AP as a tool
        """
        try:
            self._calendar_api = GoogleCalendarAPI()
            self._calendar_api.authenticate()
        except Exception as e:
            raise ValueError(f"Failed to initialize Google Calendar API: {str(e)}")
        
    def _run(self, appointment_info: str = None):
        """
        runs and schedules the appointment on to the google calendar
        """
        if not self._calendar_api:
            raise ValueError("Calendar API not initialized")
        try:
            # Convert the string to a dictionary
            input_dict = ast.literal_eval(appointment_info)
            
            # Create datetime objects from the parsed components
            start_time = datetime(
                year=int(input_dict['year']),
                month=int(input_dict['month']),
                day=int(input_dict['day']),
                hour=int(input_dict['start_hour']),
                minute=int(input_dict['start_minute'])
            )

            end_time = datetime(
                year=int(input_dict['year']),
                month=int(input_dict['month']),
                day=int(input_dict['day']),
                hour=int(input_dict['end_hour']),
                minute=int(input_dict['end_minute'])
            )
        
            # Extract other fields
            summary = input_dict.get('summary')
            description = input_dict.get('description')
            
            event_id = self._calendar_api.create_event(
                summary=summary,
                description=description,
                start_time=start_time,
                end_time=end_time
            )
            
            return f"Appointment scheduled successfully. Event ID: {event_id}"
            
        except Exception as e:
            return f"Failed to schedule appointment: {str(e)}"




