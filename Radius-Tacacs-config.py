# This script is to configure pretty much anything on cisco IOS 
# in This program it is checking if AAA config exists, if yes  then it only modifies some config items
#!/usr/bin/python3
from getpass import getpass
from cryptography.fernet import Fernet
import os
import re
import datetime
import sys
import logging
from netmiko import ConnectHandler as CH
# create Two Files first named encryption.key and p.txt
# you can either ask user to input the password or add password to password.txt
key_file_path = "FILEPATH_TO_encryption.key"
p_file_path = "FILEPATH_TO_password.txt"
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
#Generate keys
def generate_key_file():
    key = Fernet.generate_key()
    with open(key_file_path, 'wb') as file:
        file.write(key)
 
#use the keys for encryption & decryption
def use_key():
    with open(key_file_path, 'rb') as file:
        return file.read()
        
# Get the password from user.
# the password is a string, before passing to Fernet for encryption
# the plaintext has to be converted to bytes, which is why encode('utf-8').
def store_mgmt_password():
    password = getpass('Enter your password, as password is not found: ')
    key = use_key()
    fernet = Fernet(key)
    # convert the plaintext password into bytes
    # and store the encrypted byte to enc_password.
    enc_password = fernet.encrypt(password.encode('utf-8'))
    # save the encrypted password to p.txt.
    with open(p_file_path, 'wb') as file:
        file.write(enc_password)
        
       
# Decrypt the password.txt and get the plaintext password.
def get_mgmt_password():
    key = use_key()
    fernet = Fernet(key)
    with open(p_file_path, 'rb') as file:
        password_in_bytes = file.read()
    # The content in the password.txt is byte, which is why decode('utf-8') to convert to string.
    return fernet.decrypt(password_in_bytes).decode('utf-8')

# generate encrypted key by calling the above defined function.
generate_key_file()
#Then ask user to input the user password to be stored in encrypted form.
store_mgmt_password()

IP = [
	'192.168.60.10'
	]
for t in IP:
	device =  CH(device_type = 'cisco_ios', ip = t, username = 'XXXX', password = get_mgmt_password())
	output = device.send_command("sh run")
	write_file(output)
	check_AAA()
	print(device.send_command("sh run | i aaa")
	
	




