import os, time, subprocess, yaml, pathlib, threading
from sys import stdout
from datetime import datetime


##########################################[TO DO]##########################################
# VPN
#   Add in support for split tunnel vpn
#   Look in to using power shell commands in python
#       check for vpn adapter via python
#       install vpn adapter using powershell script
#   Check if VPN adapter is installed
#   Install it if not
#   set it to launch by defualt 
#   use DNS name for my MX

# Logging
#   Store 6 months worth of logs
#       store month logs in seperate files
#       delete anythin that is older
#   Store whether the Ip was last reachable in a dictionary with the IP                                     Done
#       only log on successfull ping if previous ping was unsuccessfull                                     Done
#       only log on unsuccessfull ping if previous was not successfull                                      Done
#   Store dictionary in last_status.txt                                                                     Partly
#        if ip was same copy bool, if not same defualt bool and put warning in log                          Done
#         implemant this per ns loookup / route print

# Ping 
#   Use threading for ping checks                                                                           Done
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

# Other features
#   Rename results.txt to connection_monitor
#       Set the log file and last_status.txt to be a variable declared at the top
#   Setup a file to store last status in between program restarts                                           Done
#       Read from last_status to use those variables if currently the same IP                               Done
#       Write to last_status when boolean is updated                                                        Done
#   Using the bellow command you can enable remote desktop (cmd with admin)
#       reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
#   Allow rule for icmp acrross networks would be nice :)
#   Document all the code                                                                                   Done


'''
# Need to check if defualt gateway and current ip are the same as in last_status.txt,
# if so then load the boolean 
# if not simply replace and set defualt boolean to true

'''
##########################################


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!loooooooooooook at me
# Inserted error checking that should give a error message (by calling command_failed()) if the variable we are looking gor, e.g. " 0.0.0.0" or "Address:  " is not returned by the command
# Doing this in case the device does not have internet connection and may not have a defualt route or a DNS server returned in nslookup
# line 245



##########################################[ISSUES]##########################################
# When placed in program files, gives error:
'''
Traceback (most recent call last):
  File "py_ping.pyw", line 102, in <module>
    with open("Log\\results.txt", "a+") as file: #open's the file to allow it to be written to
PermissionError: [Errno 13] Permission denied: 'Log\\results.txt'
''' 

#MAYBE FIX, i noticed the files inside the \programfiles\py monitor\ where owned by admin 
# in the mute on mute offf program they are owned by Joe and can run
# therefore copying via the setup script must retain the previous owner and permissions that work
# implement setup script to copy stuff over and see!! 

##########################################











##########################################[STARUP]##########################################
dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S") #set's the date and time to now


with open("Log\\results.txt", "a+") as file: #open's the file to allow it to be written to
    file.write("\n" + dt_string + " -- STARTUP \n")# writes to log new startup, includes date/time

#IF UNABLE TO DO THE ABOVE EXIT THE PROGRAM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# This code will create a backup dictionary and input the static values which should allways be used i ncase the last_status.txt does not exist
backup_ip_dictionary = { #Creates a backup ip dictionary with all the ip addresses needed and defualts set as reachable 
    "LoopBack" : ["127.0.0.1", True],
    "IP_Cloudflare" : ["1.1.1.1" , True],
    "IP_Google" : ["8.8.8.8" , True]
}




# This code check's whether last_status.txt exists and will load values from it if so, or create and load backup values if not
if pathlib.Path("Log\\last_status.txt").is_file(): # Does the last_status.txt exist, if so:
    last_status_exists = True
    with open('Log\\last_status.txt') as file: # Open the file
        ip_dictionary = yaml.load(file, Loader=yaml.FullLoader) # Set the contents to = ip_dictionary
        #print(ip_dictionary)

else: # If file does not exist:
    last_status_exists = False
    ip_dictionary = backup_ip_dictionary #If last_status doesnt exist then load the backup ip dictionary
    with open("Log\\last_status.txt", "w+") as file: # Creates the file if not created before
        yaml.dump(ip_dictionary, file, default_flow_style=False) #Loads in the backup to the file
        #print(ip_dictionary)
    
#IF UNABLE TO DO THE ABOVE EXIT THE PROGRAM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




        



def re_write_warning(warning_msg): # Gives warning in resulsts.txt if DNS/current ip/ defualt gateway changed
    with open("Log\\results.txt", "a+") as file: #open's the file to allow it to be written to
        file.write(dt_string + " -- WARNING -- " + warning_msg + " IP was updated \n")# writes to log new startup, includes date/time



def last_status_loop(returned_list, named_ip, output_list_placement):
# This function is resposible for iterating through last_status.txt, if there is a match with name and returned IP address from command outputs, writes it and last boolean to ip_dictionary
# If there is not a match it will write returned IP address with defualt booleans

# Variables used:
#   returned_list -- the output line, in list form, from running run_command()
#   named_ip -- the string we are trying to find from last_status.txt
#   output_list_placement -- where in the returned_list we are looking for the correct output
#   tmp_ip_dictionary -- a temporary dictionary that represents last_status.txt, loaded by yaml
#   ip_name -- the key collum for tmp_ip_dictionary
#   ip_values -- the value collum for tmp_ip_dictionary
#       ip_values[0] -- Being IP address
#       ip_values[1] -- being last state, represented in bool 
#   no_match -- a variable used to determine if a match for the named_ip and the ip_values[0]
#   last_state -- used to determine whether to use the defualt bool, or load srom last_status.txt

    with open('Log\\last_status.txt') as file: # Opens the file last_status.txt
                tmp_ip_dictionary = yaml.load(file, Loader=yaml.FullLoader) # Set the contents to = tmp_ip_dictionary
                for ip_name, ip_values in tmp_ip_dictionary.items(): #Loads the tmp_ip_dictionary with ip_name as keys and ip_values as value and iterates through each line
                    

                    if ip_name == named_ip and ip_values[0] == returned_list[1]: # If the line matches "DNS server" and the ip address returned from nslookup
                        last_state = ip_values[1] # We set the variable to equal the boolean from last_status .txt
                        no_match = False # Checking to see if we returned a match or not
                        break # This should cancel the for loop, meaning once a match is found we go straight to writing the .././

                    else: # This code will run a number of times, but since we are only setting variables it does not matter
                        last_state = True # We set the variable to equal the defualt
                        no_match = True # Checking to see if we returned a match or not

                        
                if no_match == True: # If a match was not found:
                    re_write_warning(named_ip) # Set warning message and pass it in to the re_write_warning function

                ip_dictionary[named_ip] = [returned_list[output_list_placement], last_state] #Adds the DNS server to the ip_dictionary with returned DNS IP & last_dns_server boolean
                print("Inseted in to dictionary" + returned_list[output_list_placement], last_state)
                    




def command_failed(current_loop_interface):
# This function will write an error message to the log file if the run_command() function fails the command

# Variables used:
#   dt_string -- gets the date and time for use during logging
#   current_loop_interface -- passes in what the output is expected to be, e.g. if the command is route print the expected output is "Defualt Gateway or Current IP", used if something failed
    with open("Log\\results.txt", "a+") as file:
        file.write(dt_string + " -- ERROR -- Could not load " + current_loop_interface +  " from system, current testing IP:" + "\n " + str(ip_dictionary) + " \n")





#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!loooooooooooook at me
# Inserted error checking that should give a error message (by calling command_failed()) if the variable we are looking gor, e.g. " 0.0.0.0" or "Address:  " is not returned by the command
# Doing this in case the device does not have internet connection and may not have a defualt route or a DNS server returned in nslookup
# line 245


def run_command(command, searched_var, current_loop_interface): 
# This function runs the command given, looking for searched_var. It iterates through response line by line, then splits line in to list and passes to last_status_loop()

# Variables used:
#   response -- the bytes response from running the passed in command (either nslookup or route print)
#   line -- simply represents respone split in to lines
#   command -- used to pass in which command to run
#   returned_list -- is a list of the output, showed in line, contains the wanted IP
#   searched_var -- used to narrow down the line which has the wanted IP, we iterate through line to find searched_var
#   current_loop_interface -- passes in what the output is expected to be, e.g. if the command is route print the expected output is "Defualt Gateway or Current IP", used if something failed


    new_response = ""
    response = subprocess.Popen(command, stdout=subprocess.PIPE) #Performs the route print command and set's it to equal resonse
    
    for line in iter(response.stdout.readline, ""): # iterates through each line of the response and does bellow
        line = line.decode("utf-8") # Decodes the result in to utf-8 and converts to string
        new_response = new_response + line
        if searched_var in line: # If in that section it matches " 0.0.0.0" 
            returned_list = list(line.split()) # The above string is then split into lists 


            if command == "route print":

                last_status_loop(returned_list, "Defualt_Gateway", 2) #Calling the function last_status_loop with the output from route print, looking for defualt gateway and the 2nd list item
                last_status_loop(returned_list, "Current IP", 3) #Calling the function last_status_loop with the output from route print, looking for Current IP and the 3rd list item

            elif command == "nslookup":
                last_status_loop(returned_list, "DNS server", 1) #Calling the function last_status_loop with the output from nslookup, looking for DNS server and the 1st list item

            else: #If for any reason this failes
                command_failed(current_loop_interface) #Calls the command_failed() function which writes it was not able to get current_loop_interface to log file


            break


    if searched_var not in new_response: 
        command_failed(current_loop_interface) #Calls the command_failed() function which writes it was not able to get current_loop_interface to log file


run_command("route print", " 0.0.0.0", "Defualt Gateway or Current IP") # Calling run_command function using route print and searching lines for " 0.0.0.0"
run_command("nslookup", "Address:  ", "DNS Server") # Calling run_command function using nslookup and searching lines for "Address:  "






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
# This code will ping each IP address in ip_dictionary. 
# Log if the last state was different to current, e.g. successfull ping -> unsuccessfull ping = logged // unsuccessfull ping -> successfull ping = logged
# It will also attempt and arp lookup if the ping was unsuccessfull and log.
# It also writes it's last state in 

# Variables used:
#   ip_dictionary -- stores, what entry is, IP and whether it is currently reachable
#   ip_name -- is the key collum from ip_dictionary
#   ip_values -- is the value collum from ip_dictionary
#       ip_values[0] -- Being IP address
#       ip_values[1] -- being last state, represented in bool 
#   ip -- is the 0th value from the value collum in ip_dictionary
#   response -- represents the ping output in string format
#   dt_string -- gets the date and time for use during logging
#   response_arp -- performs an arp query for ip when run
#   arp -- used to log which mac address corresponds to an IP on unsusecful ping
def ping_loop():
    while True:
        for ip_name in ip_dictionary: # Simply iterates through the ip_dictionary, entry by entry
            print(ip_name)
            ip = ip_dictionary[ip_name][0] # Set's the current IP address in loop from dictionary to ip
            response = subprocess.getoutput("ping " + ip + " -n 1") #Performs the ping command and set's it to equal resonse
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S") #set's the date and time to now



            ##### SUCCESSFULL PING
            if "Received = 1" in response and "Approximate" in response: #If there is the string "Received = 0" in the response then do:
                print(f"UP {ip} Ping Successful")
                for ip_name, ip_values in ip_dictionary.items(): # Iterates through ip_dictionary and assigns ip_dict to key and bool_dict to value
                    

                    ##### SUCCESSFULL PING & PREVIOUSLY SUCCESFULL
                    if ip == ip_values[0] and ip_values[1] == True: # If IP address mateches current in loop & was previously succesfull then:
                        #ip_dictionary.update({ip_name: [ip_values[0], True] }) # Updates the dictionary with the boolean = True in the second slot of the array within the dictionary 
                        print(str(ip_values[0]) + str(ip_values[1])) # This simply print's the current IP address: bool_dict[0] And the if it was last succesfull: bool_dict[1]



                    ##### SUCCESSFULL PING & PREVIOUSLY UNSUCCESFULL
                    elif ip == ip_values[0] and ip_values[1] == False: #If IP address mateches current in loop & was previously unsuccesfull then:
                        ip_dictionary.update({ip_name: [ip_values[0], True] }) # Updates the dictionary with the boolean = True in the second slot of the array within the dictionary 
                        print(str(ip_values[0]) + str(ip_values[1])) # This simply print's the current IP address: bool_dict[0] And the if it was last succesfull: bool_dict[1]
                        
                        with open("Log\\results.txt", "a+") as file: #open's the file to allow it to be written to
                            file.write(dt_string + " -- " + ip_name + " -- " + ip_values[0] + " Ping Successful" + "\n")# writes to log, includes date/time

                        with open('Log\\last_status.txt', 'w') as file: # Opens last_status to write
                            yaml.dump(ip_dictionary, file) #Overwrites the file with latest ip_dictionary
                        print(str(ip_dictionary))


                
            ##### UNSUCCESSFULL PING
            else: ## need to implement not successgull correctly like above
                print(f"Down {ip} Ping Unsuccessful")
                for ip_name, ip_values in ip_dictionary.items(): # Iterates through ip_dictionary and assigns ip_dict to key and bool_dict to value


                    ##### UNSUCCESSFULL PING & PREVIOUSLY UNSUCCESFULL
                    if ip == ip_values[0] and ip_values[1] == False: # If IP address mateches current in loop & was previously unsuccesfull then:
                        #ip_dictionary.update({ip_name: [ip_values[0], False] }) # Updates the dictionary with the boolean = True in the second slot of the array within the dictionary 
                        print(str(ip_values[0]) + str(ip_values[1])) # This simply print's the current IP address: bool_dict[0] And the if it was last succesfull: bool_dict[1]


                    ##### UNSUCCESSFULL PING & PREVIOUSLY SUCCESFULL
                    elif ip == ip_values[0] and ip_values[1] == True: # If IP address mateches current in loop & was previously succesfull then:
                        ip_dictionary.update({ip_name: [ip_values[0], False] }) # Updates the dictionary with the boolean = True in the second slot of the array within the dictionary 
                        print(str(ip_values[0]) + str(ip_values[1])) # This simply print's the current IP address: bool_dict[0] And the if it was last succesfull: bool_dict[1]

                        with open('Log\\last_status.txt', 'w') as file: # Opens last_status to write
                            yaml.dump(ip_dictionary, file) #Overwrites the file with latest ip_dictionary
                        print(str(ip_dictionary))

                        response_arp = subprocess.getoutput("arp -a " + str(ip)) #Performs the arp -a command with the IP address
                        if "Interface:" in response_arp: #If ip address is found in arp table
                            arp = " -- [MAC: " + response_arp.split()[10] + " ]" # Selects the MAC  address from the response and assigns it to variable  arp
                        elif "No ARP Entries Found." in response_arp: # if ip paddress is not found
                            arp = (" -- Arp not Found")

                        with open("Log\\results.txt", "a+") as file: #open's the file to allow it to be written to
                            file.write(dt_string + " -- " + ip_name + " -- " + ip_values[0] + " Ping Unsuccessful" + arp + "\n")# writes to log, includes date/time

            time.sleep(2)

##########################################


thread_ping = threading.Thread(target=ping_loop) # Declares the thread_ping to thread the function ping_loop()
thread_ping.start() # Start's the thread



''' Based on
https://github.com/labeveryday/ping_script/blob/master/tool.py
'''