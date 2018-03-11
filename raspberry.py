# Prints upcoming vehicle IDs and how many minutes away they are from a given station
from urllib2 import urlopen
import xml.etree.ElementTree as ET
import collections # Used for sorted dictionary
import sys
from blinkstick import blinkstick
import time
import datetime

#line = raw_input("What line would you like to see predictions for? ")
#stop = raw_input("What stop would you like to see a prediction for? ")

# Find Blinkstick
bstick = blinkstick.find_by_serial("BS016770-3.0")

agency = 'sf-muni'

line1 = '45'
stopNum1 = '6757' #45 stop at Union & Gough

line2 = '47'
stopNum2 = '6814' #47 stop at Van Ness & Jackson

line3 = '49'
stopNum3 = '6814' #49 stop at Van Ness & Jackson

trains = ['E','F','J','KT','L','M','N']

# Sleep timer variables
z = 25 #Steady
z1 = 1 #Blink
z2 = .65
z3 = .3
z4 = .1

def line45():

	#Get real time predictions for a stop on a route
	xml1 = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=" + agency + "&r=" + line1 + "&s=" + stopNum1)
	response1 = xml1.read()
	root1 = ET.fromstring(response1)
	for predictions in root1.iter('predictions'):
    	station1 = predictions.get('stopTitle')

	vehicles = []
	minutes = []

	for prediction in root1.iter('prediction'):
	    if line1 in trains:
	        iden = "train " + prediction.get('vehicle') + " in "
	    else:
	        iden = "bus " + prediction.get('vehicle') + " in "
	    vehicles.append(iden)
	    iden = prediction.get('minutes')
	    minutes.append(int(iden)) #Convert it to int so it sorts right later

	dictionary = dict(zip(minutes,vehicles))

	ordered_dictionary = collections.OrderedDict(sorted(dictionary.items()))

	print 'Route: ' + line1

	for x in range(0,len(dictionary)):
	    print ordered_dictionary.values()[x] + str(ordered_dictionary.keys()[x]) + ' minutes'

	# If nothing is in ordered_dictionary that means eitehr the API is down or no busses are coming
	if len(ordered_dictionary) > 0:
		light_value1 = ordered_dictionary.keys()[0]
		light_value2 = ordered_dictionary.keys()[1]

		if light_value1 <= 5:
			if light_value2 <= 20:
				actual_light = light_value2
			else:
				actual_light = light_value1
		elif light_value1 >= 6:
			actual_light = light_value1

		print 'First: ' + str(light_value1)
		print 'Second: ' + str(light_value2)
		print 'Choose: ' + str(actual_light)

		# Set to green if bus is over 15 minutes
		if actual_light >= 15:
			bstick.set_color(red=0,green=255,blue=0)
			time.sleep(z)
		# If light is between 10 and 15 minutes set to yellow
		elif actual_light < 15 and actual_light >= 10:
			bstick.set_color(red=255,green=255,blue=0)
			time.sleep(z)
		# If light is between 9 and 10 minutes slow blink red
		elif actual_light < 10 and actual_light >= 9:
			for x in range(0,(int(round((z/z1))))/2):
				bstick.set_color(red=255,green=0,blue=0)
				time.sleep(z1)
				bstick.set_color(red=0,green=0,blue=0)
				time.sleep(z1)
		# If light is between 8 and 9 minutes medium blink red
		elif actual_light < 9 and actual_light >= 8:
			for x in range(0,(int(round((z/z2))))/2):
				bstick.set_color(red=255,green=0,blue=0)
				time.sleep(z2)
				bstick.set_color(red=0,green=0,blue=0)
				time.sleep(z2)
		# If light is between 7 and 8 minutes fast blink red
		elif actual_light < 8 and actual_light >= 7:
			for x in range(0,(int(round((z/z3))))/2):
				bstick.set_color(red=255,green=0,blue=0)
				time.sleep(z3)
				bstick.set_color(red=0,green=0,blue=0)
				time.sleep(z3)
		# If light is between 6 and 7 minutes super fast blink red
		elif actual_light < 7 and actual_light >= 6:
			for x in range(0,(int(round((z/z4))))/2):
				bstick.set_color(red=255,green=0,blue=0)
				time.sleep(z4)
				bstick.set_color(red=0,green=0,blue=0)
				time.sleep(z4)
		# If light is less than or equal to 5 solid red
		elif actual_light <= 5:
			bstick.set_color(red=255,green=0,blue=0)
			time.sleep(z)
# Handle the condition where the API is down or no busses are coming (blink white)
	else:
		print 'API down or no busses available!'
		for x in range(0,(int(round((z/z3))))/2):
			bstick.set_color(red=255,green=255,blue=255)
			time.sleep(z3)
			bstick.set_color(red=0,green=0,blue=0)
			time.sleep(z3)



def line47_49():

	xml2 = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=" + agency + "&r=" + line2 + "&s=" + stopNum2)
	xml3 = urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=" + agency + "&r=" + line3 + "&s=" + stopNum3)

	response2 = xml2.read()
	response3 = xml3.read()

	root2 = ET.fromstring(response2)
	root3 = ET.fromstring(response3)

	for predictions in root2.iter('predictions'):
	    station2 = predictions.get('stopTitle')

	for predictions in root3.iter('predictions'):
	    station3 = predictions.get('stopTitle')

	vehicles = []
	minutes = []

	for prediction in root2.iter('prediction'):
	    if line2 in trains:
	        iden = "train " + prediction.get('vehicle') + " in "
	    else:
	        iden = "bus " + prediction.get('vehicle') + " in "
	    vehicles.append(iden)
	    iden = prediction.get('minutes')
	    minutes.append(int(iden)) #Convert it to int so it sorts right later

	for prediction in root3.iter('prediction'):
	    if line3 in trains:
	        iden = "train " + prediction.get('vehicle') + " in "
	    else:
	        iden = "bus " + prediction.get('vehicle') + " in "
	    vehicles.append(iden)
	    iden = prediction.get('minutes')
	    minutes.append(int(iden)) #Convert it to int so it sorts right later

	dictionary = dict(zip(minutes,vehicles))

	ordered_dictionary = collections.OrderedDict(sorted(dictionary.items()))

	print 'Routes: ' + line2 + ' & ' + line3

	for x in range(0,len(dictionary)):
	    print ordered_dictionary.values()[x] + str(ordered_dictionary.keys()[x]) + ' minutes'

	light_value1 = ordered_dictionary.keys()[0]
	light_value2 = ordered_dictionary.keys()[1]
	light_value3 = ordered_dictionary.keys()[2]

	if light_value1 < 8:
		if light_value2 < 8:
			actual_light = light_value3
		elif light_value2 >= 8:
			actual_light = light_value2
		else:
			actual_light = light_value3
	elif light_value1 >= 8:
		actual_light = light_value1

	print 'First: ' + str(light_value1)
	print 'Second: ' + str(light_value2)
	print 'Third: ' + str(light_value3)
	print actual_light

	if actual_light >= 8 and actual_light <= 10:
		bstick.set_color(red=0,green=255,blue=0)
		time.sleep(z)
	elif actual_light > 10 and actual_light <= 12:
		bstick.set_color(red=255,green=255,blue=0)
		time.sleep(z)
	elif actual_light < 8:
		bstick.set_color(red=255,green=0,blue=0)
		time.sleep(z)
	elif actual_light > 12:
		bstick.set_color(red=255,green=0,blue=0)
		time.sleep(z)

print datetime.datetime.now()

# line47_49()
# bstick.set_color(red=255,green=255,blue=255)
# time.sleep(5)
# print datetime.datetime.now()
# line47_49()

line45()
bstick.set_color(red=255,green=255,blue=255)
time.sleep(5)
print datetime.datetime.now()
line45()


# Turn off Blinkstick
bstick.turn_off()
