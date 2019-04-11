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

   # print(events_result['items'][0])    
    
    print(" ")    
    event_descriptions = []
    while True:
        selected_event = input("Would you like to know more about these events? If so, please select an event (1-10) or 'X' if there are no more events: ")
        if selected_event == "X":
            break
        if not selected_event.isdigit():
            print("Please enter a valid event number")
        if int(selected_event) not in range (1,11):
            print("Please enter a valid product id from 1 to 10")
        else:  
            event_descriptions.append(selected_event)
    
    print("* * * * * * * * * * * * * * * * *")

    #TODO: add name and number to the description 
    for selected_event in event_descriptions:
        print(events_result['items'][int(selected_event)-1]['description'])
        print("------------")

    #todo: change [0] to inputted number from user - print(events_result['items'][0]['description'])

if __name__ == '__main__':
    main()