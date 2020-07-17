# This script is to configure pretty much anything on cisco IOS 
#!/usr/bin/python3
import os
import re
import datetime
import sys
import logging
from netmiko import ConnectHandler as CH
configtopush = 'FILEPATH_FOR_FINAL_CONFIG_TO_PUSH'
def write_file(a):
	file1 = open('FILEPATH_FOR_TEMPORARY_FILE_TO_WRITE_TEMPORARY_CONFIG', "W")
	file1.write(a)
	file1.close()
def check_AAA():
	file1 = open('FILEPATH_FOR_TEMPORARY_FILE_TO_WRITE_TEMPORARY_CONFIG', "r")
	if 'aaa authentication login AUTHLIST' in file1.read():
		output = device.send_config_from_file(configtopush)
		print(output)
	file1.close()

IP = [
	'192.168.60.10'
	]
for t in IP:
	device =  CH(device_type = 'cisco_ios', ip = t, username = 'XXXX', password = 'XXXX')
	output = device.send_command("sh run")
	write_file(output)
	check_AAA()
	print(device.send_command("sh run | i aaa")
	
	
