#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import datetime
import pygsheets

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

# Initialise vars
isOpen = None
previouslyOpen = None

# Set up the door sensor pin.
DOOR_SENSOR_PIN = 18
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Open the Google Sheet to log openings
gs = pygsheets.authorize(service_file='/home/pi/service_file.json')
sh = gs.open('Letterbox Activations')
wks = sh.sheet1

firstRun = 1

while True:
    previouslyOpen = isOpen
    isOpen = GPIO.input(DOOR_SENSOR_PIN)
    if (isOpen and (isOpen != previouslyOpen)):
        now = datetime.datetime.now()
        thedate = now.strftime("%d/%m/%Y")
        thetime = now.strftime("%H:%M:%S")
        print "Letterbox has been opened! (%s at %s)" % (thedate, thetime)
	wks.add_rows(1)

	dateField = 'A%d' % wks.rows
	timeField = 'B%d' % wks.rows

	wks.cell(dateField).value = thedate
	wks.cell(timeField).value = thetime

    elif (isOpen != previouslyOpen):
        now = datetime.datetime.now()
        thedate = now.strftime("%d/%m/%Y")
        thetime = now.strftime("%H:%M:%S")
        print "Letterbox is closed. (%s at %s)" % (thedate, thetime)

	if(firstRun == 0):
	        timeClosedField = 'C%d' % wks.rows
        	wks.cell(timeClosedField).value = thetime
	else:
		firstRun = 0

    time.sleep(0.1)
