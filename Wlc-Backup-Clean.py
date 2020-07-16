#!/usr/bin/python3
import os
import re
import datetime
import sys
import logging
from netmiko import ConnectHandler as CH
# writing file in append mode
def write_file(a):
	file1 = open('FILEPATH', "a")
	file1.write(a)
	file1.close()
# IP is an list array with IP address of WLCs.
IP = ['XXX.XXX.XXX.XXX']

for t in IP:
	device =  CH(device_type = 'cisco_wlc', ip = t, username = 'XXXX', password = 'XXXX', banner_timeout=10)
        #calculate  time for  filename
	filetime = datetime.datetime.now().strftime("%H%M-%d%m%y")
        #adding time to  filename
	filename = t + "-" + filetime
# TFTP IP Need to be provided in this as SERVERIP
# List Array to send commands one at a time to CLI of WLC.
	commands = [
	'transfer upload datatype config',
	'transfer upload filename %s' % (filename),
	'transfer upload mode tftp', 
	'transfer upload path .', 
	'transfer upload serverip SERVERIP', 
	'transfer upload start', 'Y'
	]
	
	for m in commands:
		output = device.send_command_w_enter(m)
		write_file(output)
	
