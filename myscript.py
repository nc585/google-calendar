from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Google Calendar API basic functionality to pull the start time, date, and name of the next 10 events on a calendar
def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the 
    # authorization flow completes for the first time.
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
    now = datetime.datetime.utcnow().isoformat() + 'Z' #indicates UTC time
    
    print('HERE ARE THE NEXT 10 EVENTS FROM THE GEORGETOWN CALENDAR IN UTC TIME:')
    print(" ")
    events_result = service.events().list(calendarId='46gnvciofevvvsrrjpf8qri3j52njfun@import.calendar.google.com', 
                                        timeMin=now,
                                        maxResults=10, 
                                        singleEvents=True,
                                        orderBy='startTime'
                                        ).execute()
    events = events_result.get('items', [])
    i=0
    for event in events:
        i+=1
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(i,start, event['summary'])
        
    print(" ")    

    # User will input the number of the event user is interested in learning more about
    event_descriptions = []
    while True:
        selected_event = input("WOULD YOU LIKE TO KNOW MORE ABOUT THESE EVENTS? IF SO, PLEASE SELECT AN EVENT SUCH AS '1' (1-10) OR 'DONE' IF THERE ARE NO MORE EVENTS: ")
        if selected_event == "DONE":
            break
        if not selected_event.isdigit():
            print("PLEASE ENTER A VALID EVENT NUMBER.")
        if int(selected_event) not in range (1,11):
            print("PLEASE ENTER A VALID EVENT NUMBER FROM 1 TO 10.")
        else:  
            event_descriptions.append(selected_event)
    
    print(" ")
    print("* * * * * * * * * * * * * * * * *")
    
    for selected_event in event_descriptions:
        print(events_result['items'][int(selected_event)-1]['summary'])
        print(events_result['items'][int(selected_event)-1]['description'])
        print(" ")
        print("* * * * * * * * * * * * * * * * *")

    # User can create event in their personal Google calendar 
    while True:
        create_event = input("WOULD YOU LIKE TO CREATE AN EVENT REMINDER IN YOUR GOOGLE CALENDAR? IF SO, PLEASE TYPE 'YES'. IF NOT, PLEASE TYPE 'NO'.")
        if create_event == "NO":
            break
        else:  
            event_summary = input("PLEASE ENTER EVENT NAME:")
            event_location = input("PLEASE ENTER EVENT LOCATION:")
            event_desc = input("PLEASE ENTER EVENT DESCRIPTION OF YOUR CHOICE:")
            event_start = input("PLEASE ENTER EVENT START DATE IN THIS FORMAT, 'YYYY-MM-DD':")
            event_time_start = input ("PLEASE ENTER START TIME OF EVENT IN MILITARY TIME FORMAT, 'HH:MM:SS':")
            event_end = input("PLEASE ENTER EVENT END DATE IN THIS FORMAT, 'YYYY-MM-DD':")
            event_time_end = input ("PLEASE ENTER END TIME OF EVENT IN MILITARY TIME FORMAT, 'HH:MM:SS':")
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