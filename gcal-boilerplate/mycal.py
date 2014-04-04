# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line skeleton application for Calendar API.
Usage:
  $ python sample.py

You can also get help on all the command-line flags the program understands
by running:

  $ python sample.py --help

"""

import argparse
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])


# CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))

def main(argv):
  mycal = MyCalendar(argv)
  mycal.getCalendars()

class MyCalendar:

  def __init__(self, argv):
    # Parse the command-line flags.
    flags = parser.parse_args(argv[1:])

    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to the file.
    storage = file.Storage(os.path.join(os.path.dirname(__file__), 'mycal.dat'))
    credentials = storage.get()
    if credentials is None or credentials.invalid:
      credentials = tools.run_flow(FLOW, storage, flags)

    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    # Construct the service object for the interacting with the Calendar API.
    self.service = discovery.build('calendar', 'v3', http=http)

    try:
      print "Successfully authenticated your Google Account"

    except client.AccessTokenRefreshError:
      print ("The credentials have been revoked or expired, please re-run"
        "the application to re-authorize")


  #  Execute this piece of code to figure out the Test Calendar's ID once you 
  #  have created it manually in your Gcal account
  def getCalendars(self):
    calendar_list = self.service.calendarList().list().execute()
    return calendar_list

  # Try to find a calendar matching the name
  # Uses contains, not exact matching, and returns the first match
  def getCalendarId(self, name):
    calendar_list = self.getCalendars()
    for calendar_list_entry in calendar_list['items']: 
      if name in calendar_list_entry['summary']:
        return calendar_list_entry['id']

  def addEvent(self, calId, company, day):
    created_event = self.service.events().quickAdd(
      calendarId=calId,
      text='%s on %s'%(company, day)).execute()
    return created_event

  def printEvents(self, calId):
    page_token = None
    events = service.events().list(calendarId=calId, pageToken=page_token).execute()
    for event in events['items']:
      print event['summary']



if __name__ == '__main__':
  main(sys.argv)
