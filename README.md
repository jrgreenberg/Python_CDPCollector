# Python_CDPCollector
Python Script that reads in a list of IPs (routers/switches) and outputs a file that shows if a specific CDP string is matched. The purpose is to quickly find all devices (phones/APs/etc) that match the given criteria in a given network

Language = Python
Required Libraries
  sys
  time
  csv
  socket
  telnetlib
  paramiko
  
Definitions:
  ifile = .csv file to read in (IPs). Note that you could add additional columns such as username and password for each specific connection
  ofile = output doucment name
  uname = device username
  password = device password
  CDP Search String..
    for line in output1:
                	if "MS" in line:
                    change the "MS" to the your search string (ie ATA, WS-2960X, IPPHONE, etc)
                    
                    
                    
  
