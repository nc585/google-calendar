from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    print(" ")
    print("* * * * * * * * * * * * * * * * *")
    print("Welcome to the GUCal Python App!")
    print("* * * * * * * * * * * * * * * * *")
    print(" ")

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Here are the next 10 events in the Georgetown Calendar:')
    print(" ")
    events_result = service.events().list(calendarId='46gnvciofevvvsrrjpf8qri3j52njfun@import.calendar.google.com', 
                                        timeMin=now,
                                        maxResults=10, 
                                        singleEvents=True,
                                        orderBy='startTime'
                                        ).execute()
    events = events_result.get('items', [])
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # TODO: add an event number if possible
        print(start, event['summary'])
        
    print(" ")    
    event_descriptions = []
    while True:
        selected_event = input("Would you like to know more about these events? If so, please select an event (1-10) or 'DONE' if there are no more events: ")
        if selected_event == "DONE":
            break
        if not selected_event.isdigit():
            print("Please enter a valid event number.")
        if int(selected_event) not in range (1,11):
            print("Please enter a valid event number from 1 to 10.")
        else:  
            event_descriptions.append(selected_event)
    
    print("* * * * * * * * * * * * * * * * *")

    #TODO: add name and number to the description 
    for selected_event in event_descriptions:
        print(events_result['items'][int(selected_event)-1]['description'])
        print("------------")

#TODO: give user option to create event reminder
    while True:
        create_event = input("Would you like to create an event reminder in your Google calendar? If so, please type 'YES'. If not, please type 'NO'.")
        if create_event == "NO":
            break
        else:  
            event_summary = input("Please enter event name:")
            event_location = input("Please enter event location:")
            event_desc = input("Please enter event description of your choice:")
            event_start = input("Please enter event start date in the following format, YYYY-MM-DD:")
            event_time_start = input ("Please enter start time of event in the following format, HH-MM-SS:")
            event_end = input("Please enter event end date in the following format, YYYY-MM-DD:")
            event_time_end = input ("Please enter end time of event in the following format, HH-MM-SS:")
            event = {
                'summary': event_summary,
                'location': event_location,
                'description': event_desc,
                'start': {
                    'dateTime': event_start + 'T' + event_time_start, 
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'dateTime': event_end + 'T' + event_time_end, 
                    'timeZone': 'America/New_York',
                },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    main()