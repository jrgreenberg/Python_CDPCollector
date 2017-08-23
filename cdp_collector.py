#Required Libraries
import paramiko
import telnetlib
import sys
import time
import csv
import socket

#Variable Definitions
ifile = csv.DictReader(open("testIP.csv"))
ofile = "testoutput.txt"
target = open(ofile,'w')
fieldname = ['IP']
TELNET_PORT = 23
SSH_PORT = 22
TELNET_TIMEOUT = 6
READ_TIMEOUT = 6
header = 0

#Reads in the ifile CSV document
for row in ifile:
	if header is 0:
		#DEBUG - Prints the Key Values
		print row.keys()
		header = 1
	ipaddr = row["IP"]

	#Defines the username and password for the connections
	#This could be incorporated into the ifile
	uname = 'test'
	password = 'test'
	
	#Tests to see if the router/switch will accept SSH connections. If it does the connection will proceed as SSH, otherwise it will proceed as telnet
	try:
		test_conn = telnetlib.Telnet(ipaddr,SSH_PORT,TELNET_TIMEOUT)

	#Socket error = SSH not supported, Use telnet	
	except socket.error:
		
		#Debug Message
		print("SSH not available, using Telnet")
		
		#Creates the telnet connection
		remote_conn = telnetlib.Telnet(ipaddr,TELNET_PORT,TELNET_TIMEOUT)
		
		#Expect-like script to collect username and password
		output = remote_conn.read_until("sername:", TELNET_TIMEOUT)
		remote_conn.write(uname + '\n')
		output = remote_conn.read_until("assword:", TELNET_TIMEOUT)
		remote_conn.write(password +  '\n')
		
		#Reads all data in buffer
		time.sleep(1)
		output = remote_conn.read_very_eager()
		
		#Sets term length to 0
		remote_conn.write("term le 0" + "\n")
		time.sleep(3)
		output = remote_conn.read_very_eager()
		
		#Used to gather hostname for the output
		remote_conn.write("show run | inc hostname" + "\n")
		time.sleep(4)
		hostname = remote_conn.read_very_eager()
		hostname = hostname.split('\n')
		for line in hostname:
			if "hostname" in line:
				hostname1 = line
			else:
				continue  
		hostname1 = hostname1.strip('hostname')
		
		#Debug Message
		print(hostname1)
		
		#Finally, the Show CDP neighbors command 
		remote_conn.write("show cdp neighbors" + "\n")
		time.sleep(3)
		
		output = remote_conn.read_very_eager()
        	output1= output.split("\n")
        	target.write(str(hostname1))
		target.write('\n')
		#Goes line-by-line through the output of the CDP neighbors command. 
		#Change the "MS" to desired search string for example ATA, IPPhone, AP, etc.   
		for line in output1:
                	if "MS" in line:
                			#Debug Message
                        	print(line)
                                target.write(str(line))
                                target.write("\n")
                target.write("____________________________________________________________________\n")


    #SSH test worked, Use SSH
	else: 
		print("SSH is working")
	
		#SSH Session establishment
		remote_conn_pre = paramiko.SSHClient()
		remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		remote_conn_pre.connect(ipaddr,username=uname,password=password)
		
		#Inovkes interactive shell with established SSH connection
		remote_conn=remote_conn_pre.invoke_shell()
		output = remote_conn.recv(5000)
		
		#Same command structure as above (telent section), different syntax
		remote_conn.send("\n")
		remote_conn.send("term le 0\n")
		time.sleep(1)
		output = remote_conn.recv(100)
		remote_conn.send("\n")
		time.sleep(1)
		hostname = remote_conn.recv(100)
		hostname = hostname.strip('#')
		remote_conn.send("show cdp nei\n")
		time.sleep(1)
		output = remote_conn.recv(65535)
		output1= output.split("\n")
		target.write(str(hostname))
		target.write("\n")
		for line in output1:
                        if "MS" in line:
                                print(line)
                                target.write(str(line))
                                target.write("\n")
		target.write("____________________________________________________________________\n")
