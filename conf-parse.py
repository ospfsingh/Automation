# This Script is used to parse NxOS,IOS,ASA config and find out the interface 
# Addresses, to help document the what IPs are used where and in which
# Vrf, This can be modified to itrate over the folder where all the 
# backup configs are stored and find all kinds of information.
# i like it this way instead of running scripts on Live environment.

from ciscoconfparse import CiscoConfParse
import re
import os
# Folder where the back up confgs are stored.
folder = '/home/thinkpad/Downloads'
#parseing the file.

for subdir, dirs, files in os.walk(folder):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + file
        #need to test TRY-EXCEPT section
		try:
			parse = CiscoConfParse(filepath, syntax='nxos')
		except:
			try:
			parse = CiscoConfParse(filepath, syntax='ios')
			except:
				parse = CiscoConfParse(filepath, syntax='asa')

	#printing the hostname
	print(parse.find_lines('^hostname', exactmatch=False, ignore_ws=False))

	#For loop for finding the all the interfaces and itrating over them.
	for intf_obj in parse.find_objects('^interface'):
		intf_name = intf_obj.re_match_typed('^interface\s+(\S.+?)$')
		# Search children of all interfaces for a regex match and return
		# the value matched in regex match group 1.  If there is no match,
		# return a default value: ''
		intf_ip_addr1 = intf_obj.re_match_iter_typed(
			r'ip\saddress\s(\d+\.\d+\.\d+\.\d+\/\d+)', result_type=str,
			group=1, default='')
		vrf_member = intf_obj.re_match_iter_typed(
			r'(vrf\smember\s[a-zA-Z-]{0,50})', result_type=str,
			group=1, default='')
		shutdown = intf_obj.re_match_iter_typed(
			r'(no\sshut[a-zA-Z-]{0,50})', result_type=str,
			group=1, default='')
		print("{0}: {1}: {2}: {3}".format(intf_name, intf_ip_addr, 
			vrf_member, shutdown))



