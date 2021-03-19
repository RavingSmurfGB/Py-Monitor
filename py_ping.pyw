import os, time, subprocess
from datetime import datetime


##########################################[TO DO]##########################################
#
# Add in support for split tunnel vpn
#   Look in to using power shell commands in python
#       check for vpn adapter via python
#       install vpn adapter using powershell script
#   Check if VPN adapter is installed
#   Install it if not
#   set it to launch by defualt 
#   use DNS name for my MX

# Work on ping logging
#   Store 6 months worth of logs
#       store month logs in seperate files
#       delete anythin that is older
#   Store whether the Ip was last reachable in a dictionary with the IP                                     Done
#       only log on successfull ping if previous ping was unsuccessfull                                     Done
#       only log on unsuccessfull ping if previous was not successfull                                      Done

# Ping 
#   Use threading for ping checks
#   Check for current active IP and add it to the ip_dictionary                                             Done
#   Check for the current defualt gateway and add it to the ip_dictionary                                   Done
#   Check for the current DNS server and add it to the ip_dictionary
#       Also leave a log statement showing that this is the, current_ip, defualt_gateway & DNS server       Partly
#   Check arp table for ip address if recieved failed responde
#       Then log accorgingly

# DNS 
#   Try to do a nslookup for google, yahoo etc..
#       only log on not connect if previous log was connect
#       only log on connect if previous was not connect


##########################################




##########################################[ISSUES]##########################################
# When placed in program files, gives error:
'''
Traceback (most recent call last):
  File "py_ping.pyw", line 102, in <module>
    with open("Log\\results.txt", "a+") as file: #open's the file to allow it to be written to
PermissionError: [Errno 13] Permission denied: 'Log\\results.txt'
'''
# Unsuccesful ping s cause duplicates

##########################################







##########################################[IP DETECTION & SETUP]##########################################

ip_dictionary = { #Creates an dictionary with all the ip addresses needed and whether they are currently reachable
    "LoopBack" : ["127.0.0.1", False],
    "IP_Cloudflare" : ["1.1.1.1" , True],
    "IP_Google" : ["8.8.8.8" , True],
    "TEST UNSECCEFUL" : ["125.0.0.1", True]
}



response = subprocess.Popen("route print", stdout=subprocess.PIPE) # set's the variable response as the returned info from route print
for line in iter(response.stdout.readline, ""): # iterates through each line of the response and does bellow
    line = line.decode("utf-8") # Decodes the result in to utf-8 and converts to string
    if ' 0.0.0.0' in line: # If in that section it matches " 0.0.0.0" 
        returned_ip_list = list(line.split()) # The above string is then split into lists 
        ip_dictionary["Defualt_Gateway"] = [returned_ip_list[2], True] # We select the Defualt gateway from the list
        ip_dictionary["Current IP"] = [returned_ip_list[3], True] # We select the Current IP from the list
        break 

'''
response_dns = subprocess.Popen("nslookup", stdout=subprocess.PIPE)
for line in iter(response_dns.stdout.readline, ""): # iterates through each line of the response and does bellow
    line = line.decode("utf-8") # Decodes the result in to utf-8 and converts to string
'''


##########################################










##########################################[Ping Logic & logging]##########################################
while True:
    for ip_name in ip_dictionary: 
        ip = ip_dictionary[ip_name][0] # Set's the current IP address in loop from dictionary to ip
        response = os.popen(f"ping {ip} -n 1").read() # response is called 
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S") #set's the date and time to now



        ##### SUCCESSFULL PING
        if "Received = 1" in response and "Approximate" in response: #If there is the string "Received = 0" in the response then do:
            print(f"UP {ip} Ping Successful")
            for ip_name, ip_values in ip_dictionary.items(): # Iterates through ip_dictionary and assigns ip_dict to key and bool_dict to value
                

                ##### SUCCESSFULL PING & PREVIOUSLY SUCCESFULL
                if ip == ip_values[0] and ip_values[1] == True: # If IP address mateches current in loop & was previously succesfull then:
                    ip_dictionary.update({ip_name: [ip_values[0], True] }) # Updates the dictionary with the boolean = True in the second slot of the array within the dictionary 
                    print(str(ip_values[0]) + str(ip_values[1])) # This simply print's the current IP address: bool_dict[0] And the if it was last succesfull: bool_dict[1]


                ##### SUCCESSFULL PING & PREVIOUSLY UNSUCCESFULL
                elif ip == ip_values[0] and ip_values[1] == False: #If IP address mateches current in loop & was previously unsuccesfull then:
                    ip_dictionary.update({ip_name: [ip_values[0], True] }) # Updates the dictionary with the boolean = True in the second slot of the array within the dictionary 
                    print(str(ip_values[0]) + str(ip_values[1])) # This simply print's the current IP address: bool_dict[0] And the if it was last succesfull: bool_dict[1]
                    with open("Log\\results.txt", "a+") as file: #open's the file to allow it to be written to
                        file.write(dt_string + " -- " + ip_name + " -- " + ip_values[0] + " Ping Successful" + "\n")# writes to log, includes date/time


            
        ##### UNSUCCESSFULL PING
        else: ## need to implement not successgull correctly like above
            print(f"Down {ip} Ping Unsuccessful")
            for ip_name, ip_values in ip_dictionary.items(): # Iterates through ip_dictionary and assigns ip_dict to key and bool_dict to value


                ##### UNSUCCESSFULL PING & PREVIOUSLY SUCCESFULL
                if ip == ip_values[0] and ip_values[1] == True: # If IP address mateches current in loop & was previously succesfull then:
                    ip_dictionary.update({ip_name: [ip_values[0], False] }) # Updates the dictionary with the boolean = True in the second slot of the array within the dictionary 
                    print(str(ip_values[0]) + str(ip_values[1])) # This simply print's the current IP address: bool_dict[0] And the if it was last succesfull: bool_dict[1]


                ##### UNSUCCESSFULL PING & PREVIOUSLY UNSUCCESFULL
                elif ip == ip_values[0] and ip_values[1] == False: # If IP address mateches current in loop & was previously unsuccesfull then:
                    ip_dictionary.update({ip_name: [ip_values[0], False] }) # Updates the dictionary with the boolean = True in the second slot of the array within the dictionary 
                    print(str(ip_values[0]) + str(ip_values[1])) # This simply print's the current IP address: bool_dict[0] And the if it was last succesfull: bool_dict[1]
                    with open("Log\\results.txt", "a+") as file: #open's the file to allow it to be written to
                        file.write(dt_string + " -- " + ip_name + " -- " + ip_values[0] + " Ping Unsuccessful" + "\n")# writes to log, includes date/time

        time.sleep(2)

##########################################






''' Based on
https://github.com/labeveryday/ping_script/blob/master/tool.py
'''