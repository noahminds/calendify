from __future__ import print_function

import os
import os.path
import datetime as dt
import openai
import re
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask


SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Please specify your default timezone formatted as an IANA Time Zone Database name:
defaultTimeZone = "Europe/Madrid"

#
# Start_or_End
#
class Start_or_End:
    def __init__(self, dateTime, timeZone) -> None:
        self.dateTime = dateTime
        self.timeZone = timeZone

    def editDateTime(self, newDateTime) -> None:
        self.dateTime = newDateTime

    def editTimeZone(self, newTimeZone) -> None:
        self.timeZone = newTimeZone

    def getDateTime(self):
        return [self.dateTime, self.timeZone]

#
# Event
#
class Event:
    def __init__(self, title, location, description, start : Start_or_End, end : Start_or_End) -> None:
        self.title = title
        self.location = location
        self.description = description
        self.start = start
        self.end = end
    
    def editTitle(self, newTitle) -> None:
        self.title = newTitle

    def editLocation(self, newLocation) -> None:
        self.location = newLocation

    def editDescription(self, newDescription) -> None:
        self.description = newDescription

    def editStartTime(self, newStartTime) -> None:
        self.start.editDateTime(newStartTime)

    def editEndTime(self, newEndTime) -> None:
        self.start.editDateTime(newEndTime)

    def editTimeZone(self, newTimeZone) -> None:
        self.start.editTimeZone(newTimeZone)
        self.end.editTimeZone(newTimeZone)

    def getTitle(self) -> str:
        return self.title
    
    def getLocation(self) -> str:
        return self.location
    
    def getDescription(self) -> str:
        return self.description
    
    def getStart(self):
        return self.start.getDateTime()
    
    def getEnd(self):
        return self.end.getDateTime()
    
    def printEvent(self):
        print(f"- Title: {self.title}")
        print(f"- Location: {self.location}")
        print(f"- Description: {self.description}")
        print(f"- Start Date(Time): {self.start.getDateTime()[0]}, {self.start.getDateTime()[1]}")
        print(f"- Start Date(Time): {self.end.getDateTime()[0]}, {self.end.getDateTime()[1]}\n")

#
# calendarPush
#
# Takes a list of events and creates calendar invites for each event
# using the google calendar API 
def calendarPush(event : Event, creds) -> None:
    # to_push = events.getEvents()
    service = build("calendar", "v3", credentials=creds)

    # if len(to_push) == 0:
    #     print("No events to push")
    #     return
    
    print("Pushing event to calendar...")
    try:
        event = {
            'summary': event.getTitle(),
            'location': event.getLocation(),
            'description': event.getDescription(),
            'start' : {
                'dateTime': event.getStart()[0],
                'timeZone': event.getStart()[1]
            },
            'end' : {
                'dateTime' : event.getEnd()[0],
                'timeZone' : event.getEnd()[1]
            },
            'reminders' : {
                'useDefault': False,
                'overrides': [
                {'method': 'popup', 'minutes': 60},
                ],
            },
        }
            
        calId = "e1205b4ff7417aa6aece23057a10daeedaeb114732adc03d60e25d8e17624cda@group.calendar.google.com"
        event = service.events().insert(calendarId=calId, body=event).execute()
        print(f"Event successfully created: {event.get('htmlLink')}", )

    except HttpError as error:
        print("An error occurred:", error)


# Function to analyze event description using the GPT API
def analyze_event_description(event_description, api_key):
    # Set the GPT API key
    openai.api_key = api_key

    # Priming instructions for extracting event information
    primer = """
You are a helpful assistant that is given event descriptions and extracts the relevant information in the specified format:

Input:
"{EVENT_DESCRIPTION}"

Expected Output:
- Title: {TITLE}
- Location: {LOCATION}
- Description: {DESCRIPTION}
- Start Date(Time): {DATE(TIME)}
- End Date(Time): {DATE(TIME)}

Note: If the event is recurring, the "Start Date(Time)" and "End Date(Time)" fields should contain the respective start or end date and time of the first occurrence of the event.
Note: Don't include timezone information in the output.
Note: The description should be concise and informative, summarizing purpose, goals, and other relevant information.
"""

    # Sample event descriptions and outputs for priming the GPT API
    example_event_description1 = """
This week is Employer Week! 
Day: January 10, 11 and 12 (Tue, Wed and Thu)
Time: 1-4pm
Location: Ford Design Center Ground Floor Lobby

Looking for an opportunity to talk with representatives from a variety of companies? This is an informal event to network and learn more about these companies. Find out what engineer roles they have, if they have any openings and what their hiring process is.
Companies in attendance will include:
ActiveCampaign
Epic
IMC Trading
"""

    example_output1 = """
- Title: Employer Week
- Location: Ford Design Center Ground Floor Lobby
- Description: Informal networking event to explore engineer roles, job openings, and hiring processes from various companies.
- Start Date(Time): 2023-01-10T13:00:00
- End Date(Time): 2023-01-10T16:00:00
"""

    example_event_description2 = """
Hi Bob,
Register today for the NCA Winter Career Fair!
The fair will be virtual on Wednesday, February 1, 9:00-11:30 AM, CT.
Once you register, you will receive prep emails, can build your fair day schedule, and will learn more about attending employers.
"""

    example_output2 = """
- Title: NCA Winter Career Fair
- Location: Virtual
- Description: Virtual career fair for students to meet with employers.
- Start Date(Time): 2023-02-01T09:00:00
- End Date(Time): 2023-02-01T11:30:00
"""

    example_event_description3 = """
Building Hippo: A Healthcare Price Comparison Web App from Idea to Launch (hosted by Chris)

When: Thursday 4/13 @ 6:00 - 7:00 PM at Tech M164 and via Zoom (link here)
"""

    example_output3 = """
- Title: Building Hippo: A Healthcare Price Comparison Web App from Idea to Launch
- Location: Tech M164 and via Zoom
- Description: Seminar hosted by Chris on the process of building and launching a healthcare price comparison web app called Hippo.
- Start Date(Time): 2023-04-13T18:00:00
- End Date(Time): 2023-04-13T19:00:00
"""

    # The business jargon translation example, but with example names for the example messages
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": primer},
            {"role": "system", "name":"example_user", "content": example_event_description1},
            {"role": "system", "name": "example_assistant", "content": example_output1},
            {"role": "system", "name":"example_user", "content": example_event_description2},
            {"role": "system", "name": "example_assistant", "content": example_output2},
            {"role": "system", "name":"example_user", "content": example_event_description3},
            {"role": "system", "name": "example_assistant", "content": example_output3},
            {"role": "user", "content": event_description}
        ],
        temperature=0.2,
        max_tokens=150
    )

    usage = response["usage"]
    formatted_event = response["choices"][0]["message"]["content"]

    if usage["total_tokens"] > 1200:
        print("WARNING: Token use was significant!\n" + usage + "\n")

    pattern = re.compile("^(\n|)- Title: .+\n- Location: .+\n- Description: .+\n- Start Date\(Time\): [0-9]{4}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]\n- End Date\(Time\): [0-9]{4}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$")

    if not pattern.search(formatted_event):
        print("Uh Oh! Incorrectly formatted output:\n" + formatted_event + "\n")
        raise ValueError("Unable to process your event description. Please try again ensuring that the exact date (MM/DD), start & end times, and an event description are provided in your input...\n")

    # Extract relevant information from the response
    event_data = {}
    lines = response["choices"][0]["message"]["content"].split("\n")
    for line in lines:
        key, value = line.split(": ", 1)
        event_data[key.strip(" -")] = value

    event = Event(event_data.get("Title"),
                  event_data.get("Location"),
                  event_data.get("Description"),
                  Start_or_End(event_data.get("Start Date(Time)"), defaultTimeZone),
                  Start_or_End(event_data.get("End Date(Time)"), defaultTimeZone))
    
    return event

def inputEvent(api_key) -> Event:
    print("Please write or paste your event description. To submit or exit please press Enter followed by CTRL+D (CTRL+Z on Windows):")
    
    lines_str = ''
    lines = []
    while True:
        try:
            lines.append(input())
        
        except EOFError:
            lines_str = '\n'.join(lines)
            
            if len(lines_str) > 1200:
                print(f"\n\nInput exceeded character limit: {len(lines_str)}/1200 characters")
                print(f"Please try again...\n")

                lines = []
                lines_str = ''

                print("Please write or paste your event description. To submit or exit please press Enter followed by CTRL+D (CTRL+Z on Windows):")
                continue
            
            break
    
    if lines_str.strip() == '':
        sys.exit()
    else:
        print("\nEvent description submitted! Processing...\n")

    try:
        formatted_event = analyze_event_description(lines_str, api_key)
        formatted_event.printEvent()
        return formatted_event
        
    except ValueError as error:
        print("An error occured: ", error)
        formatted_event = inputEvent(api_key)
        return formatted_event

# Function to reformat start and end times using the GPT API
def reformat_times(dateTime, api_key) -> str:
    # Set the GPT API key
    openai.api_key = api_key

    # Priming instructions for reformatting times
    primer = "You are a helpful assistant that is given a date and time and reformats it to the specified format YYYY-MM-DDTHH:MM:SS"
    example_event1 = "Thursday 4/13 @ 6:00 PM"
    example_output1 = "2023-04-13T18:00:00"
    example_event2 = "September 3rd, 4:15pm CT"
    example_output2 = "2023-09-03T16:15:00"

    # The business jargon translation example, but with example names for the example messages
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": primer},
            {"role": "system", "name":"example_user", "content": example_event1},
            {"role": "system", "name": "example_assistant", "content": example_output1},
            {"role": "system", "name":"example_user", "content": example_event2},
            {"role": "system", "name": "example_assistant", "content": example_output2},
            {"role": "user", "content": dateTime}
        ],
        temperature=0.2,
        max_tokens=30
    )

    return response["choices"][0]["message"]["content"]


#
# editEvent
#
def editEvent(event : Event, api_key):
    count = 0
    
    # Loop until user is done editing
    while True:
        # If count is greater than 0 then display the edited event details
        if count > 0:
            print("\nHere is your updated event:")
            event.printEvent()

        # Prompt user to select an event field to edit using field number pairs
        print("Please select an event field to edit by typing the corresponding number and pressing Enter. Otherwise, if you are done editing, please type '6' and press Enter.")
        print("Title (1), Location (2), Description (3), Start Date(Time) (4), End Date(Time) (5), Timezone (6) || Exit (7)")
        field = input("Number: ")

        if field.strip().lower() == '7':
            if count == 0:
                print("No changes were made to the event. Exiting...")
                break
            else:
                print("All changes saved. Exiting...\n")
                break

        elif field.strip() == '1':
            newTitle = input("Please enter a new title and press Enter: ")
            event.editTitle(newTitle)
            print("Title successfully updated!")
            count += 1

        elif field.strip() == '2':
            newLocation = input("Please enter a new location and press Enter: ")
            event.editLocation(newLocation)
            print("Location successfully updated!")
            count += 1

        elif field.strip() == '3':
            newDescription = input("Please enter a new description and press Enter: ")
            event.editDescription(newDescription)
            print("Description successfully updated!")
            count += 1

        elif field.strip() == '4':
            newStart = input("Please enter a new start date and time (no specific format) and press Enter: ")
            
            # Reformat the new start time using the GPT API
            formatted_newStart = reformat_times(newStart, api_key).strip()

            # Check that the new start time was formatted correctly
            pattern = re.compile("^[0-9]{4}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$")
            if not pattern.search(formatted_newStart):
                print("Invalid input. Please try again and ensure you specify the year, month, day, and start time...")
                count = 0
                continue

            # Check that the new start time is before the end time
            if formatted_newStart.strip() >= event.getEnd()[0]:
                print("Invalid input. Start time must be before end time. Please try again...")
                count = 0
                continue

            event.editStartTime(formatted_newStart.strip())
            print("Start date and time successfully updated!")
            count += 1

        elif field.strip() == '5':
            newEnd = input("Please enter a new end date and time (no specific format) and press Enter: ")

            # Reformat the new end time using the GPT API
            formatted_newEnd = reformat_times(newEnd, api_key).strip()

            # Check that the new end time was formatted correctly
            pattern = re.compile("^[0-9]{4}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$")
            if not pattern.search(formatted_newEnd):
                print("Invalid input. Please try again and ensure you specify the year, month, day, and end time...")
                count = 0
                continue

            # Check that the new end time is after the start time
            if formatted_newEnd.strip() <= event.getStart()[0]:
                print("Invalid input. End time must be after start time. Please try again...")
                count = 0
                continue

            event.editEndTime(formatted_newEnd.strip())
            print("End date and time successfully updated!")
            count += 1

        elif field.strip() == '6':
            newTimeZone = input("Please enter a new timezone formatted as an IANA Time Zone Database name and press Enter: ")
            event.editTimeZone(newTimeZone.strip())
            print("Timezone successfully updated!")
            count += 1

        else:
            print("Invalid input. Please try again...")
            count = 0
            continue


def main():
    # Retrieve the GPT API key from the environment variable
    api_key = os.environ.get("OPENAI_API_KEY")

    # Check if the GPT API key is set
    if not api_key:
        raise ValueError("API key not found. Set the OPENAI_API_KEY environment variable.")

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    event = inputEvent(api_key)

    while True:
        action = input("If you are ready to submit your event to your calendar, please type 'done' and press Enter. Otherwise, to modify your event details, please type 'edit', press Enter, and follow the instructions: ")
        
        if action.strip().lower() == 'done':
            calendarPush(event, creds)
            print("\nEvent successfully added to your calendar! To create a new event please run the program again. Goodbye!\n")
            break
        elif action.strip().lower() == 'edit':
            editEvent(event, api_key)
        else:
            print("Invalid input. Please try again...")
            continue


if __name__ == "__main__":
    main()
