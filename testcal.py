#!/usr/bin/python

'''
Basic tests for calendar api
'''

import sys
import os

sys.path.append('gcal-boilerplate')
from mycal import MyCalendar


def main(argv):
	mc = MyCalendar(argv)
	testGetCalendars(mc)
	testGetCalendarId(mc, "Test Calendar")
	calId = mc.getCalendarId("Test Calendar")
	testAddEvent(mc, calId, "AXP", "16-Apr-14")


def testGetCalendars(mc):
	calendar_list = mc.getCalendars()
	for calendar_list_entry in calendar_list['items']:
		print calendar_list_entry['summary']


def testGetCalendarId(mc, name):
	calendar = mc.getCalendarId(name)
	print 'The calendar is %s'%(calendar)


def testAddEvent(mc, calId, company, day):
	created_event = mc.addEvent(calId, company, day)
	print 'Successfully Created event %s %s'%(created_event['summary'], created_event['id'])


if __name__ == '__main__':
  main(sys.argv)
