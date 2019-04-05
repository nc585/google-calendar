# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
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

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    
    #list available Google calendars in the user account
    # page_token = None
    # calendar_list = service.calendarList().list(pageToken=page_token).execute()
    # for calendar_list_entry in calendar_list['items']:
    #     print(calendar_list_entry['summary'])


    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='46gnvciofevvvsrrjpf8qri3j52njfun@import.calendar.google.com', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    #events = events_result.get('items', [])
    for event in events_result['items']:
        print(event['summary'])
        #print(events_result['items'])
        #print(events_result['items']['id'])

#https://developers.google.com/calendar/v3/reference/events/move 
    # updated_event = service.events().move(
    #     calendarId='46gnvciofevvvsrrjpf8qri3j52njfun@import.calendar.google.com', eventId='eventId',
    #     destination='primary').execute()


    temp = "georgetown.edu_s8ptv0o8fqh92oqard457uojm4@group.calendar.google.com"

    # First retrieve the event from the API.
    updated_event = service.events().move(
        calendarId='primary', 
        eventId='MTJsYms0c25uNmxhamxoN2NjZWkydjRyYXAgbmM1ODVAZ2VvcmdldG93bi5lZHU',
        destination=temp
    ).execute()

# Print the updated date.
    print(updated_event['updated'])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

    # page_token = None
    # while True:
    #     events = service.events().list(calendarId='primary', pageToken=page_token).execute()
    #     for event in events['items']:
    #         print(event['summary'])
    #     page_token = events.get('nextPageToken')
    #     if not page_token:
    #         break

    # calendar_list_entry = service.calendarList().get(calendarId='calendarId').execute()
    # print(calendar_list_entry['summary'])

    event_option = {
        'summary': 'Google I/O 2015',
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': '2019-04-28T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2019-04-28T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        # 'recurrence': [
        #     'RRULE:FREQ=DAILY;COUNT=2'
        # ],
        # 'attendees': [
        #     {'email': 'lpage@example.com'},
        #     {'email': 'sbrin@example.com'},
        # ],
        # 'reminders': {
        #     'useDefault': False,
        #     'overrides': [
        #     {'method': 'email', 'minutes': 24 * 60},
        #     {'method': 'popup', 'minutes': 10},
        #     ],
        # },
    }

    # event = service.events().insert(calendarId='primary', body=event_option).execute()
    # print(type(event))
    # print('Event created: %s' % (event.get('htmlLink')))





if __name__ == '__main__':
    main()
# [END calendar_quickstart]