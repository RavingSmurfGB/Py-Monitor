import os, time, subprocess, yaml, pathlib
from sys import stdout
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
#   Check for the current DNS server and add it to the ip_dictionary                                        Done
#       Also leave a log statement showing that this is the, current_ip, defualt_gateway & DNS server       Done
#   Check arp table for ip address if recieved failed responde                                              Done
#       Then log accorgingly                                                                                Done
#   Error check, implement for DNS, Defualt gateway and ARP
#       If value is not ' 0.0.0.0' in defualt gateway code for e.g. , code will crash currently


# DNS 
#   Try to do a nslookup for google, yahoo etc..
#       only log on not connect if previous log was connect
#       only log on connect if previous was not connect

# Rename results.txt to connection_monitor
# Setup a file to store last status in between program restarts                                             Partly

##########################################




##########################################[ISSUES]##########################################
# When placed in program files, gives error:
'''
Traceback (most recent call last):
  File "py_ping.pyw", line 102, in <module>
    with open("Log\\results.txt", "a+") as file: #open's the file to allow it to be written to
PermissionError: [Errno 13] Permission denied: 'Log\\results.txt'
'''

##########################################











##########################################[STARUP]##########################################
dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S") #set's the date and time to now
with open("Log\\results.txt", "a+") as file: #open's the file to allow it to be written to
    file.write("\n" + dt_string + " -- STARTUP \n")# writes to log new startup, includes date/time



# This code will create a backup dictionary and input the static values which should allways be used i ncase the last_status.txt does not exist
backup_ip_dictionary = { #Creates a dictionary with all the ip addresses needed and defualts to reachable 
    "LoopBack" : ["127.0.0.1", True],
    "IP_Cloudflare" : ["1.1.1.1" , True],
    "IP_Google" : ["8.8.8.8" , True]
}


# This code check's weather last_status.txt and will load values from it if so, or create and load backup values if not
if pathlib.Path("Log\\last_status.txt").is_file(): # Does the last_status.txt exist, if so:
    last_status_exists = True
    with open('Log\\last_status.txt') as file: # Open the file
        ip_dictionary = yaml.load(file, Loader=yaml.FullLoader) # Set the contents to = ip_dictionary
        print(ip_dictionary)

else: # If file does not exist:
    last_status_exists = False
    ip_dictionary = backup_ip_dictionary #If last_status doesnt exist then load the backup ip dictionary
    with open("Log\\last_status.txt", "w+") as file: # Creates the file if not created before
        yaml.dump(ip_dictionary, file, default_flow_style=False) #Loads in the backup to the file
        print(ip_dictionary)


        
# Need to check if defualt gateway and current ip are the same as in last_status.txt,
# if so then load the boolean 
# if not simply replace and set defualt boolean to true


# This code will query the defualt gateway and currently used IP and add it to the dictionary
response = subprocess.Popen("route print", stdout=subprocess.PIPE) #Performs the route print command and set's it to equal resonse
for line in iter(response.stdout.readline, ""): # iterates through each line of the response and does bellow
    line = line.decode("utf-8") # Decodes the result in to utf-8 and converts to string
    if ' 0.0.0.0' in line: # If in that section it matches " 0.0.0.0" 
        returned_ip_list = list(line.split()) # The above string is then split into lists 
        ip_dictionary["Defualt_Gateway"] = [returned_ip_list[2], True] # We select the Defualt gateway from the list
        ip_dictionary["Current IP"] = [returned_ip_list[3], True] # We select the Current IP from the list
        break 


# This code will query the defualt gateway and currently used DNS server and add it to the dictionary
response_dns = subprocess.Popen("nslookup", stdout=subprocess.PIPE) #Performs the nslookup command and set's it to equal resonse_dns
for line in iter(response_dns.stdout.readline, ""): # iterates through each line of the response and does bellow
    line = line.decode("utf-8") # Decodes the result in to utf-8 and converts to string
    if "Address:  " in line: # If in that section it matches "Address:  "
        returned_DNS_list = list(line.split()) #The above string is then split into lists 
        ip_dictionary["DNS server"] = [returned_DNS_list[1], True]
        break


##########################################




''' CODE DID NOT WORK, alwwyas didnt return anything??
response_arp = subprocess.system("arp -a " + str(ip), stdout=subprocess.PIPE) #Performs the nslookup command and set's it to equal resonse_dns
for line in iter(response_arp.stdout.readline, ""): # iterates through each line of the response and does bellow
    line = line.decode("utf-8") # Decodes the result in to utf-8 and converts to string
    print(str(line))

    if "Interface:" in line: ############################### BREAKS ON THIS LINE;;; Is unable to find Interface: due to the above not returning anything
        response_arp = list(line.split()) #The above string is then split into lists 
        print(response_arp)
        break
    print("coudlnt find arp!!")
    break

#### EVEN THIS DOESNT RETURN ANYTHING :()
with os.system('arp -a') as f:
    data = f.read()
'''







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


                ##### UNSUCCESSFULL PING & PREVIOUSLY UNSUCCESFULL
                if ip == ip_values[0] and ip_values[1] == False: # If IP address mateches current in loop & was previously unsuccesfull then:
                    ip_dictionary.update({ip_name: [ip_values[0], False] }) # Updates the dictionary with the boolean = True in the second slot of the array within the dictionary 
                    print(str(ip_values[0]) + str(ip_values[1])) # This simply print's the current IP address: bool_dict[0] And the if it was last succesfull: bool_dict[1]


                ##### UNSUCCESSFULL PING & PREVIOUSLY SUCCESFULL
                elif ip == ip_values[0] and ip_values[1] == True: # If IP address mateches current in loop & was previously succesfull then:
                    ip_dictionary.update({ip_name: [ip_values[0], False] }) # Updates the dictionary with the boolean = True in the second slot of the array within the dictionary 
                    print(str(ip_values[0]) + str(ip_values[1])) # This simply print's the current IP address: bool_dict[0] And the if it was last succesfull: bool_dict[1]

                    response_arp = subprocess.getoutput("arp -a " + str(ip)) #Performs the arp -a command with the IP address
                    if "Interface:" in response_arp: #If ip address is found in arp table
                        arp = " -- [MAC: " + response_arp.split()[10] + " ]" # Selects the MAC  address from the response and assigns it to variable  arp
                    elif "No ARP Entries Found." in response_arp: # if ip paddress is not found
                        arp = (" -- Arp not Found")

                    with open("Log\\results.txt", "a+") as file: #open's the file to allow it to be written to
                        file.write(dt_string + " -- " + ip_name + " -- " + ip_values[0] + " Ping Unsuccessful" + arp + "\n")# writes to log, includes date/time

        time.sleep(2)

##########################################






''' Based on
https://github.com/labeveryday/ping_script/blob/master/tool.py
'''