#!/usr/bin/python

import os
import time
import sys, getopt
import httplib, urllib
import ctypes
import re

def main(argv):
	key = ''
	try:
		opts, args = getopt.getopt(argv,"hk:",["key="])
	except getopt.GetoptError:
		print 'counter.py -k <thingspeak api key>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'counter.py -k <thingspeak api key>'
			sys.exit()
		elif opt in ("-k", "--key"):
			key = arg
	if len(argv) < 1:
		print 'counter.py -k <thingspeak api key>'
		sys.exit()

	os.system('modprobe w1-gpio pullup=1')
	os.system('modprobe w1_ds2423')
	sensor = '/sys/bus/w1/devices/1d-0000000f9d60/w1_slave'
	loop(key, sensor)

def raw_data(sensor):
	f = open(sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

def loop(key, sensor):
	while True:
		time.sleep(60)
		lines = raw_data(sensor)
		index = 0
		a = 0
		b = 0
		for line in lines:
			before, crc, count = line.partition('crc=YES c=')
			re.sub('[^a-zA-Z0-9-_*.]', '', count)
			if (index == 2):
				a = count
				print("{}: {}".format('A', count))
			if (index == 3):
				b = count
				print("{}: {}".format('B', count))
			index += 1
		thingspeak(key, a, b)

def thingspeak(key, a, b):
	params = urllib.urlencode({'field1': a, 'field2': b, 'key': key})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept":"text/plain"}
	try:
		conn = httplib.HTTPConnection("api.thingspeak.com:80")
		conn.request("POST", "/update", params, headers)
		response = conn.getresponse()
		print response.status, response.reason
		print ''
		data = response.read()
		conn.close()
	except Exception as e:
		print 'Error occured when sending data to ThingSpeak.', e.message

if __name__ == "__main__":
	main(sys.argv[1:])
