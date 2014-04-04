#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib2 
import csv
import sys
sys.path.append('gcal-boilerplate')
from mycal import MyCalendar

"""

Scraper for earnings dates using Yahoo Finance
Usage:
  $ python earnings.py Your-CSV-File-Here

Where the CSV file contains all the different tickers
for the earnings dates you wish to retrieve

Example CSV file:

AXP, American Express Inc.
INTC, Intel Corporation
..
..
..

"""

class EarningsDateCalculator:

    companies = []
    companiesdict = {}

    def printdate(self, symbol):
        print symbol
        print self.getdate(symbol)

    def getdate(self, symbol):
        request_url = "http://finance.yahoo.com/q?s=%s"%symbol
        page = urllib2.urlopen(request_url)
        soup = BeautifulSoup(page.read())
        infotable = soup.find(id="table1")
        infocells = infotable.find_all('td', "yfnc_tabledata1")
        earningsdate = infocells[6].contents[0]
        return earningsdate
    
    def getAllDates(self):
        for sym in self.companies:
            self.printdate(sym)

    def __init__(self, csvfile):
        f = open(csvfile, 'rU')
        try:
            reader = csv.reader(f)
            for row in reader:
                # print row
                self.companiesdict[row[0]] = row[1]
        finally:
            f.close()

        # print self.companiesdict
        self.companies = self.companiesdict.keys()
        # print "Done reading in the dict"
        # print self.companies


def main(argv):
    # TODO: Make this safe and user friendly and shit
    csvfile = argv[1]
    calendarName = argv[2]
    
    # Initialize yahoo scraper and google calendar services
    ec = EarningsDateCalculator(csvfile)
    cal = MyCalendar(argv[3:])
    testCalendarId = cal.getCalendarId(calendarName)

    # Generate and add calendar events
    for symbol in ec.companies:
        description = ec.companiesdict[symbol]
        date = ec.getdate(symbol)
        created_event = cal.addEvent(testCalendarId, "%s,%s"%(symbol,description), date)
        print 'Successfully Created event %s %s'%(created_event['summary'], created_event['id'])


if __name__ == "__main__":
    main(sys.argv)
