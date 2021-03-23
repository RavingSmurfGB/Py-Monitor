import os, time, subprocess, yaml, pathlib, threading
from sys import stdout
from datetime import datetime


##########################################[TO DO]##########################################
# VPN
#   Add in support for split tunnel vpn                                                                     Done
#   check for vpn adapter via python                                                                        Done
#       install vpn adapter                                                                                 Done                                                       
#   Check if VPN adapter is installed                                                                       Done
#   Install it if not                                                                                       Done
#   set it to launch by defualt                                                                             Done
#   use DNS name for my MX                                                                                  Done
#   Store VPN's last connection                                                                    
#        if ip was same not log, if different log

# Logging
#   Store 6 months worth of logs                                                                            Partly
#       store month logs in seperate files                                                                  Done
#       delete anythin that is older
#   Store whether the Ip was last reachable in a dictionary with the IP                                     Done
#       only log on successfull ping if previous ping was unsuccessfull                                     Done
#       only log on unsuccessfull ping if previous was not successfull                                      Done
#   Store dictionary in last_status.txt                                                                     Done
#        if ip was same copy bool, if not same defualt bool and put warning in log                          Done
#         implemant this per ns loookup / route print                                                       Done

# Ping 
#   Use threading for ping checks                                                                           Done
#   Check for current active IP and add it to the ip_dictionary                                             Done
#   Check for the current defualt gateway and add it to the ip_dictionary                                   Done
#   Check for the current DNS server and add it to the ip_dictionary                                        Done
#       Also leave a log statement showing that this is the, current_ip, defualt_gateway & DNS server       Done
#   Check arp table for ip address if recieved failed responde                                              Done
#       Then log accorgingly                                                                                Done



# DNS 
#   Try to do a nslookup for google, yahoo etc..                                                            Done
#       only log on not connect if previous log was connect                                                 Done
#       only log on connect if previous was not connect                                                     Done





# Other features
#   Move respective last_status.txts into a different folder and update code
#   Rename results.txt to connection_monitor                                                                Done
#       Set the log file and last_status.txt to be a variable declared at the top                           Done
#   Setup a file to store last status in between program restarts                                           Done
#       Read from last_status to use those variables if currently the same IP                               Done
#       Write to last_status when boolean is updated                                                        Done
#   Using the bellow command you can enable remote desktop (cmd with admin)
#       reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
#   windows firewall Allow rule for icmp acrross networks would be nice :)
#   Document all the code                                                                                   Done

# Error checking
#   error check to see if backup dictionaries are at least contained in respective last_status.txt          Done

#   Error check, implement for DNS, Defualt gateway and ARP
#       If value is not ' 0.0.0.0' in defualt gateway code for e.g. , code will crash currently
#
#   if ping recieves Reply from 192.168.3.30: Destination host unreachable.
#       and the ip within that string is not the same as the current one, perhaps re-do ip check at startup to modify the ip_dictionary
#       may have to then update ip_dictionary in thread someway


##########################################





##########################################[ISSUES]##########################################
#When device does not have internet connection, program hangs!!!!!!!!!!!!!!!!!!!!!

#implement error checking for file creation!!

#re_write_warning not working in last_status_loop() allways triggers when should not

# When placed in program files, gives error:
'''
Traceback (most recent call last):
  File "py_ping.pyw", line 102, in <module>
    with open(log_file, "a+") as file: #open's the file to allow it to be written to
PermissionError: [Errno 13] Permission denied: 'Log\\results.txt'
''' 

#MAYBE FIX, i noticed the files inside the \programfiles\py monitor\ where owned by admin 
# in the mute on mute offf program they are owned by Joe and can run
# therefore copying via the setup script must retain the previous owner and permissions that work
# implement setup script to copy stuff over and see!! 

##########################################













##########################################[STARUP]##########################################
vpn_enabled = True # Used to enable or disable VPN control

ip_last_status_log = "Log\\ip_last_status.txt" # Creates a variable that stores the last_status info for ip_dictionary
dns_last_status_log = "Log\\dns_last_status.txt" # Creates a variable that stores the last_status info for dns_dictionary


date_string = datetime.now().strftime("%Y_%m_") #creates a year_month string for use in creating log file
log_file = "Log\\" + date_string + "connection_monitor.txt" # sets log file to be current month + connection_monitor.txt



dt_string = datetime.now().strftime("/%Y/%m/%d %H:%M:%S") #set's the date and time to now


with open(log_file, "a+") as file: #open's the file to allow it to be written to
    file.write("\n" + dt_string + " -- STARTUP \n")# writes to log new startup, includes date/time
#NEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEED to insert error checking if the file cannot be read, also log error if so



# This code will create a backup dictionary and input the static values which should allways be used i ncase the ip_last_status.txt does not exist
backup_ip_dictionary = { #Creates a backup ip dictionary with all the ip addresses needed and defualts set as reachable 
    "LoopBack" : ["127.0.0.1", True],
    "IP_Cloudflare" : ["1.1.1.1" , True],
    "IP_Google" : ["8.8.8.8" , True]
}

backup_dns_dictionary = {
    "google.com" : True,
    "yahoo.com" : True,
    "aws.amazon.com" : True
}




def write_backup_dictionary(current_last_status, current_dictionary):
#This function simply overwirtes what is in current_last_status

#Variables used:
#   current_last_status -- Is either ip_last_status_log or dns_last_status_log
#   current_dictionary -- Is the dictionary to be written to file (will overwrite)

    with open(current_last_status, "w+") as file: # Creates the file if not created before
        yaml.dump(current_dictionary, file, default_flow_style=False, sort_keys=False) #Loads in the backup to the file


#NEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEED to insert error checking if a file cannot be created
def check_last_status(current_last_status, backup_dictionary):
# This function is used to check if the last_status.txt exists  
# If so then it will load values from it
# If not it will load backup 

#Variables used:
# current_last_status -- contains either ip_last_status_log or dns_last_status_log
# backup_dictionary -- contains either backup_ip_dictionary or backup_dns_dictionary
# current_dictionary -- contains either dns_dictionary or ip_dictionary & returns the loaded dictionary

    # This code check's whether ip_last_status.txt exists and will load values from it if so, or create and load backup values if not
    if pathlib.Path(current_last_status).is_file(): # Does the last_status.txt exist, if so:

        if os.stat("Log\\ip_last_status.txt").st_size == 0: # Check if file is empty
            print("file is empty")
            current_dictionary = backup_dictionary # if file is empty, load backup_dictionary,
            write_backup_dictionary(current_last_status, current_dictionary) # Overwtire 

        else:
            with open(current_last_status) as file: # Open the file as read
                tmp_current_last_status = yaml.load(file, Loader=yaml.FullLoader) # Set the contents to = tmp_current_dictionary

                if str(tuple(backup_dictionary.keys())).strip('(' + ')') in str(tuple(tmp_current_last_status.keys())).strip('(' + ')'): # This checks whether the keys of backup_dictionary is contained in the loaded file 

                    current_dictionary = tmp_current_last_status # on one loop this makes ip_dictionary what is read from the file, then it does the same for dns_dictionary
                else: 
                    current_dictionary = backup_dictionary # if file is empty, load backup_dictionary, file last_status will be overwitten later on 
                    write_backup_dictionary(current_last_status, current_dictionary)

    else: # If file does not exist:
        current_dictionary = backup_dictionary # Set's the current_dictionary to be the backup_dictionary
        write_backup_dictionary(current_last_status, current_dictionary)


    return current_dictionary

ip_dictionary = check_last_status(ip_last_status_log, backup_ip_dictionary)
dns_dictionary = check_last_status(dns_last_status_log, backup_dns_dictionary)




def check_create_vpn():
# This function checks if the vpn has been created if not, it will create it
# This function is called every time vpn_reconnection is

# Variables used:
#   vpn_exists -- used to determine if vpn exists or not 

    response = subprocess.getoutput('powershell -command " Get-VpnConnection  Home-Split-Tunnel"' ) #Performs the ping command and set's it to equal resonse
    if "Name                  : Home-Split-Tunnel" in response:
        vpn_exists = True
    elif "Name                  : Home-Split-Tunnel" not in response:
        subprocess.getoutput('powershell -command "Add-VpnConnection  -Name "Home-Split-Tunnel" -ServerAddress "j-wired-mnrjwwgrzz.dynamic-m.com-mnrjwwgrzz.dynamic-m.com"  -TunnelType "L2tp" -L2tpPsk "Elements" -Force -EncryptionLevel "Optional" -AuthenticationMethod Pap,Chap,MSChapv2 -RememberCredential -SplitTunneling"' ) #Performs the ping command and set's it to equal resonse
        subprocess.getoutput('powershell -command "Add-VpnConnectionRoute -ConnectionName "Home-Split-Tunnel" -DestinationPrefix 192.168.0.0/24 "' )
        with open(log_file, "a+") as file: #open's the file to allow it to be written to
            file.write(dt_string + " -- MESSAGE -- VPN was created \n")# writes to log new startup, includes date/time
        vpn_exists = True
    else:
        vpn_exists = False

        #log here on vpn not able to be created
        #   only if this is the first instance though
        #   if has failed to be created before ignore
        '''
        with open(log_file, "a+") as file: #open's the file to allow it to be written to
            file.write(dt_string + " -- WARNING -- VPN could not be created \n")# writes to log new startup, includes date/time
        '''

    return vpn_exists
##########################################








##########################################[UPDATING IP ADDRESSES]##########################################

def re_write_warning(warning_msg): # Gives warning in resulsts.txt if DNS/current ip/ defualt gateway changed
    with open(log_file, "a+") as file: #open's the file to allow it to be written to
        file.write(dt_string + " -- WARNING -- " + warning_msg + " IP was updated \n")# writes to log new startup, includes date/time



def last_status_loop(returned_list, named_ip, output_list_placement):
# This function is resposible for iterating through ip_last_status.txt, if there is a match with name and returned IP address from command outputs, writes it and last boolean to ip_dictionary
# If there is not a match it will write returned IP address with defualt booleans

# Variables used:
#   returned_list -- the output line, in list form, from running run_command()
#   named_ip -- the string we are trying to find from ip_last_status.txt
#   output_list_placement -- where in the returned_list we are looking for the correct output
#   tmp_ip_dictionary -- a temporary dictionary that represents ip_last_status.txt, loaded by yaml
#   ip_name -- the key collum for tmp_ip_dictionary
#   ip_values -- the value collum for tmp_ip_dictionary
#       ip_values[0] -- Being IP address
#       ip_values[1] -- being last state, represented in bool 
#   no_match -- a variable used to determine if a match for the named_ip and the ip_values[0]
#   last_state -- used to determine whether to use the defualt bool, or load srom ip_last_status.txt
    
    with open(ip_last_status_log) as file: # Opens the file ip_last_status.txt
        
        tmp_ip_dictionary = yaml.load(file, Loader=yaml.FullLoader) # Set the contents to = tmp_ip_dictionary
        
        for ip_name, ip_values in tmp_ip_dictionary.items(): #Loads the tmp_ip_dictionary with ip_name as keys and ip_values as value and iterates through each line
            #print("got here!")

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
        #print("Inseted in to dictionary" + returned_list[output_list_placement], last_state)
                    




def command_failed(current_loop_interface):
# This function will write an error message to the log file if the run_command() function fails the command

# Variables used:
#   dt_string -- gets the date and time for use during logging
#   current_loop_interface -- passes in what the output is expected to be, e.g. if the command is route print the expected output is "Defualt Gateway or Current IP", used if something failed
    with open(log_file, "a+") as file:
        file.write(dt_string + " -- ERROR -- Could not load " + current_loop_interface +  " from system, current testing IP:" + "\n " + str(ip_dictionary) + " \n")


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


    if searched_var not in new_response or " UnKnown" in new_response: 
        command_failed(current_loop_interface) #Calls the command_failed() function which writes it was not able to get current_loop_interface to log file


run_command("route print", " 0.0.0.0", "Defualt Gateway or Current IP") # Calling run_command function using route print and searching lines for " 0.0.0.0"
run_command("nslookup", "Address:  ", "DNS Server") # Calling run_command function using nslookup and searching lines for "Address:  "

##########################################






'''
with open(ip_last_status_log) as file: # Opens last_status to write
    
    dictionaries = yaml.dump(yaml.load(file))
    for dictionary in dictionaries:
        print(str(dictionary))

'''











##########################################[VPN RECONNECTION & LOGGING]##########################################
def vpn_reconnection():
# This function will loop, to check if the VPN is connected, if not it will connect it
# If the VPN is not created it will also check this and create it

# Variables used:
#   vpn_exists -- is the return in bool from check_create_vpn()

    while True:
        vpn_exists = check_create_vpn()        

        if vpn_exists == True:
            response = subprocess.getoutput("rasdial.exe ") #Performs the ping command and set's it to equal resonse
            if "Home-Split-Tunnel" in response:
                print("VPN is already connected")


            elif "No connections" in response:
                print("VPN is not connected")
                connect = subprocess.getoutput("rasdial.exe Home-Split-Tunnel Unattended_Devices74jg5@protonmail.com Elements") #Performs the ping command and set's it to equal resonse

                if "Successfully connected to Home-Split-Tunnel." in connect:
                    print("Connected to the VPN")

                    # log here if was able to connect
                    #   only log if was previously unsucessfull at connecting

                else:
                    print("was not able to connect to vpn")

                    # log here if not able to connect 
                    #   only log here if was previously succesfull at connecting


        elif vpn_exists == False:
            print("could not connect to vpn")


        time.sleep(600) # sleep for ten minutes


##########################################





##########################################[PING TEST & LOGGING]##########################################
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
            dt_string = datetime.now().strftime("/%Y/%m/%d %H:%M:%S") #set's the date and time to now



            ##### SUCCESSFULL PING
            if "Received = 1" in response and "Approximate" in response: #If there is the string "Received = 0" in the response then do:
                print("UP " + ip + " Ping Successful")
                for ip_name, ip_values in ip_dictionary.items(): # Iterates through ip_dictionary and assigns ip_dict to key and bool_dict to value
                    


                    ##### SUCCESSFULL PING & PREVIOUSLY UNSUCCESFULL
                    if ip == ip_values[0] and ip_values[1] == False: #If IP address mateches current in loop & was previously unsuccesfull then:
                        ip_dictionary.update({ip_name: [ip_values[0], True] }) # Updates the dictionary with the boolean = True in the second slot of the array within the dictionary 
                        print(str(ip_values[0]) + str(ip_values[1])) # This simply print's the current IP address: bool_dict[0] And the if it was last succesfull: bool_dict[1]
                        
                        with open(log_file, "a+") as file: #open's the file to allow it to be written to
                            file.write(dt_string + " -- " + ip_name + " -- " + ip_values[0] + " Ping Successful" + "\n")# writes to log, includes date/time

                        with open(ip_last_status_log, 'w') as file: # Opens last_status to write
                            yaml.dump(ip_dictionary, file, sort_keys=False) #Overwrites the file with latest ip_dictionary
                        print(str(ip_dictionary))


                
            ##### UNSUCCESSFULL PING
            else: ## need to implement not successgull correctly like above
                print("Down " + ip + " Ping Successful")
                for ip_name, ip_values in ip_dictionary.items(): # Iterates through ip_dictionary and assigns ip_dict to key and bool_dict to value


                    ##### UNSUCCESSFULL PING & PREVIOUSLY SUCCESFULL
                    if ip == ip_values[0] and ip_values[1] == True: # If IP address mateches current in loop & was previously succesfull then:
                        ip_dictionary.update({ip_name: [ip_values[0], False] }) # Updates the dictionary with the boolean = True in the second slot of the array within the dictionary 
                        print(str(ip_values[0]) + str(ip_values[1])) # This simply print's the current IP address: bool_dict[0] And the if it was last succesfull: bool_dict[1]

                        with open(ip_last_status_log, 'w') as file: # Opens last_status to write
                            yaml.dump(ip_dictionary, file, sort_keys=False) #Overwrites the file with latest ip_dictionary
                        print(str(ip_dictionary))

                        response_arp = subprocess.getoutput("arp -a " + str(ip)) #Performs the arp -a command with the IP address
                        if "Interface:" in response_arp: #If ip address is found in arp table
                            arp = " -- [MAC: " + response_arp.split()[10] + " ]" # Selects the MAC  address from the response and assigns it to variable  arp
                        elif "No ARP Entries Found." in response_arp: # if ip paddress is not found
                            arp = (" -- Arp not Found")

                        with open(log_file, "a+") as file: #open's the file to allow it to be written to
                            file.write(dt_string + " -- " + ip_name + " -- " + ip_values[0] + " Ping Unsuccessful" + arp + "\n")# writes to log, includes date/time

            time.sleep(2)
##########################################









##########################################[DNS TEST & LOGGING]##########################################
def nslookup_loop():
    while True:
        for dns_name in dns_dictionary:
            print(dns_name)
            response = subprocess.getoutput("nslookup " + dns_name ) #Performs the ping command and set's it to equal resonse
            dt_string = datetime.now().strftime("/%Y/%m/%d %H:%M:%S") #set's the date and time to now


            ##### SUCCESSFULL RESOLVE
            if "Non-authoritative answer:" in response:  
                print("UP " + dns_name + " DNS Resolve Successful")
                for dns_dictionary_name, dns_dictionary_last_status in dns_dictionary.items(): # Iterates through dns_dictionary and assigns dns_name to key and dns_last_status to value
                    
                    
                    ##### SUCCESSFULL RESOLVE & PREVIOUSLY UNSUCCESSFULL
                    if dns_name == dns_dictionary_name and dns_dictionary_last_status == False: # If dns dictionary entry matches current current DNS name and was previously unsuccessfull
                        dns_dictionary.update({dns_name : True}) # Updates the dns dictionary entry for current DNS, setting to true
                        print(dns_dictionary_name + str(dns_dictionary_last_status)) # Print latest info from dns dictionary

                        with open(log_file, "a+") as file: #open's the file to allow it to be appended
                            file.write(dt_string + " -- " + "DNS Resolve" + " -- " + dns_dictionary_name + " DNS Resolve Successful" + "\n")# writes to log, includes date/time

                        with open(dns_last_status_log, 'w') as file: # Opens last_status to write
                            yaml.dump(dns_dictionary, file, sort_keys=False) #Overwrites the file with latest ip_dictionary
                        print(str(dns_dictionary))
            
            

            ##### UNSUCCESSFULL RESOLVE
            else:
                print("DOWN " + dns_name + " DNS Resolve Unsuccessful")
                for dns_dictionary_name, dns_dictionary_last_status in dns_dictionary.items(): # Iterates through dns_dictionary and assigns dns_name to key and dns_last_status to value
                    

                    ##### UNSUCCESSFULL RESOLVE & PREVIOUSLY SUCCESSFULL
                    if dns_name == dns_dictionary_name and dns_dictionary_last_status == True: # If dns dictionary entry matches current current DNS name and was previously unsuccessfull
                        dns_dictionary.update({dns_name : False}) # Updates the dns dictionary entry for current DNS, setting to true
                        print(dns_dictionary_name + str(dns_dictionary_last_status)) # Print latest info from dns dictionary

                        with open(log_file, "a+") as file: #open's the file to allow it to be appended
                            file.write(dt_string + " -- " + "DNS Resolve" + " -- " + dns_dictionary_name + "  DNS Resolve Unsuccessful" + "\n")# writes to log, includes date/time

                        with open(dns_last_status_log, 'w') as file: # Opens last_status to write
                            yaml.dump(dns_dictionary, file, sort_keys=False) #Overwrites the file with latest ip_dictionary
                        print(str(dns_dictionary))


            time.sleep(1)
##########################################







##########################################[MAIN]##########################################
thread_ping = threading.Thread(target=ping_loop) # Declares the thread_ping to thread the function ping_loop()
thread_nslookup = threading.Thread(target=nslookup_loop) # Declares the thread_nslookup to the function nslookup_loop()
thread_vpn = threading.Thread(target=vpn_reconnection) # Declares the thread_vpn to the function vpn_reconnection()

thread_ping.start() 
thread_nslookup.start() 

if vpn_enabled == True:
    thread_vpn.start()


##########################################


''' Based on
https://github.com/labeveryday/ping_script/blob/master/tool.py
'''