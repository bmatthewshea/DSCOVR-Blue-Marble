#!/usr/bin/python3

# DSCOVR: Deep Space Climate Observatory :
# Earth Polychromatic Imaging Camera
# Daily Blue Marble API:
# https://epic.gsfc.nasa.gov/about/api
# Python Script by: Brady Shea
# 27 August 2019

import sys, json
from urllib.request import urlopen
from datetime import date

url_base  = "https://epic.gsfc.nasa.gov/"
most_recent = url_base + "api/natural"

# start functions

def pretty_date(iyear, imonth, iday):
  return date(month=imonth, day=iday, year=iyear).strftime('%B %d, %Y')

def find_most_recent_date():
  print('\nContacting API to find newest image date available..')
  try:
    data = urlopen(most_recent)
    jdata = json.loads(data.read())
    for x in jdata:
      most_recent_date = x['identifier']
  except:
    print('\n\nConnection problem! Could not find most recent images. Using default of 6/27/2019..\n\n')
    most_recent_date = "20190627000000"
  most_recent_date = most_recent_date[:-6] #strip last 5 chars from date string found
  return most_recent_date

def do_image_list(imagetype):
  api = url_base + "api/{}/date/{}-{}-{}".format(imagetype, Year, Month, Day)
  archive = url_base + "archive/{}/{}/{}/{}/png/".format(imagetype, Year, Month, Day)
  try:
    data = urlopen(api)
    jdata = json.loads(data.read())
    print(imagetype.capitalize() + " images available for {}{}{}:".format(Year, Month, Day))
    for x in jdata:
      print(archive + x['image'] + '.png')
    print("\n")
  except:
    print('Problem with connection. Exiting.')

# end functions

# Start main logic

print('\nDSCOVR: Deep Space Climate Observatory \"Blue Marble\" Image Query Utility')

end_date = find_most_recent_date()
cYear  = end_date[:4]
cMonth = end_date[4:6]
cDay   = end_date[6:]
formatted_end_date = '-'.join([end_date[:4], end_date[4:6], end_date[6:]])

print('The most recent images have been detected on {}'.format(pretty_date( int(cYear), int(cMonth), int(cDay) )) + '..\n')

# Ask user for dates (valid date: 20150704 thru 20190627) -> EDIT: 20190627-20200301 is unavailabe (Back online as of 2MARCH2020)
try:
  input_date = input('Enter a date in YYYY-MM-DD format (2015-07-04 thru ' + formatted_end_date + ') (Press Enter for most recent): ')
  if ( input_date == "" ): # user hit enter - no input
    Year  = cYear;  y = int(Year)
    Month = cMonth; m = int(Month)
    Day   = cDay;   d = int(Day)
    print("No input. Using the most recent date found: {}.".format(pretty_date(y, m, d)))
  else: # found user input
    Year, Month, Day = map(str, input_date.split('-')) # Need strings to maintain '01-09' as str instead of single digit int.
    y, m, d =          map(int, input_date.split('-')) # same, but int's for datetime
except:
  print("Invalid Input. Exiting.")
  sys.exit(1)
print('\nQuerying API for images on {}'.format(pretty_date(y, m, d)) + '..\n')
#natural
do_image_list("natural")
#enhanced
do_image_list("enhanced")
sys.exit(0)
