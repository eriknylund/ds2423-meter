#!/usr/bin/python

import os
import time
import sys, getopt
import httplib, urllib
import yaml

config = ''

def main(argv):
	configfile = 'config.yml'
	try:
		opts, args = getopt.getopt(argv,"hc:",["config="])
	except getopt.GetoptError:
		print 'counter.py -c <config.yml file>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'counter.py -c <config.yml file>'
			sys.exit()
		elif opt in ("-c", "--config"):
			configfile = arg

	with open(configfile, 'r') as stream:
		try:
			global config
			config = yaml.load(stream)
			print "Config loaded from {}.".format(configfile)
		except yaml.YAMLError as exc:
			print(exc)

	os.system('modprobe w1-gpio pullup=1')
	os.system('modprobe w1_ds2423')
	print("1-wire configured.")
	loop()

def read_ds2423():
	sensor = "/sys/bus/w1/devices/{}/w1_slave".format(config['device-id'])
	f = open(sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

def loop():
	while True:
		lines = read_ds2423()
		index = 0
		a = 0
		b = 0
		for line in lines:
			before, crc, count = line.partition('crc=YES c=')
			count = float(count.rstrip())
			if (index == 2):
				a = count / config['counter-a']['impulses-per-kwh']
				print("{}: {}".format('A', a))
			if (index == 3):
				b = count / config['counter-b']['impulses-per-kwh']
				print("{}: {}".format('B', b))
			index += 1
		thingspeak(a, b)
		time.sleep(config['delay-seconds'])

def thingspeak(a, b):
	key = config['thingspeak-api-key']
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
