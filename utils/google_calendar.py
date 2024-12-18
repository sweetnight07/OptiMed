# import other packages
import os
from dotenv import load_dotenv
import datetime
import pickle

# import google packages
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class GoogleCalendarAPI:
    def __init__(self):
        """
        initializes the scope and sets up the environment to access to the token and cred
        """
        # set up environment, accessing files outside directory 
        self._setup_environment()
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.creds = None
        self.service = None

    def _setup_environment(self):
        """load environment variables and set workspace directory and optionally returns keys."""
        load_dotenv()
        workspace_directory = os.getenv('WORKSPACE_DIRECTORY')

        if not workspace_directory:
            raise ValueError("WORKSPACE_DIRECTORY not set in environment variables")
        
        os.chdir(workspace_directory)

    def authenticate(self, credentials_path='credentials.json', token_path='token.pickle'):
        """authenticate users with google calendar api using OAuth 2.0"""
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)
            
        # after extracting the tokens.pickle, is it valid
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # need to access the credentials 
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.SCOPES)
                # access this scope with the credential and see if its valid
                self.creds = flow.run_local_server(port=0)
            # serializes the object self.creds into the token which is the path
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)
        # service is available
        self.service = build('calendar', 'v3', credentials=self.creds)

    def create_event(self, summary: str = "Doctor Appointment",
                     description: str = "Appointment Description",
                     start_time: datetime = None,
                     end_time: datetime = None,
                     timezone: str = "America/New_York"):
        """
        schedules the apppointment onto the google calendar
        """
        if not self.service:
            raise ValueError("Please authenticate first using authenticate()")

        # we need to confirt the start time into the iso format
        start_time_str = start_time.isoformat()
        end_time_str = end_time.isoformat()

        # build the body that will be passed into the calendar as a service
        event = {
            'summary': summary,
            'description' : description,
            'start': {
                'dateTime': start_time_str,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time_str,
                'timeZone': timezone
            },
        }

        # make the calendar appointment service
        try:
            event = self.service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
            return event['id']
        except Exception as e:
            raise Exception(f"Failed to create event: {str(e)}")