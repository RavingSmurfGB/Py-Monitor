import yaml



backup_ip_dictionary = { #Creates a backup ip dictionary with all the ip addresses needed and defualts set as reachable 
    "LoopBack" : ["127.0.0.1", True],
    "IP_Cloudflare" : ["1.1.1.1" , True],

}





with open("Log\\ip_last_status.txt") as file: # Open the file as read
    ip_dictionary = yaml.load(file, Loader=yaml.FullLoader) # Set the contents to = tmp_current_dictionary

print("backup_ip_dictionary -- " + str(tuple(backup_ip_dictionary.keys())).strip('(' + ')'))
print("ip_dictionary        -- " + str(tuple(ip_dictionary.keys())).strip('(' + ')'))




if str(tuple(backup_ip_dictionary.keys())).strip('(' + ')') in str(tuple(ip_dictionary.keys())).strip('(' + ')'):
    print("YAY")



