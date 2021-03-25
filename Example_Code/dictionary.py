import yaml


# Create a dictionary of dictionaries
MAIN_dictionary = {"backup_ip_dictionary": {"LoopBack" : ["127.0.0.1", True],
            "IP_Cloudflare" : ["1.1.1.1" , True],
            "IP_Google" : ["8.8.8.8" , True]},

          2: {'Name': 'Marie', 'Age': '22', 'Sex': 'Female'}}

'''
print(people[1]) #reading nested dictionary
print(people[1]['age']) #reading specific key from nested dictionary
'''

print(MAIN_dictionary["backup_ip_dictionary"])

MAIN_dictionary[3] = {}

#writing to nested dictionary
MAIN_dictionary[3]['name'] = 'Luna'
MAIN_dictionary[3]['age'] = '24'



# create another nested dictionary
MAIN_dictionary[4] = {'name': 'Peter', 'age': '29', 'sex': 'Male', 'married': 'Yes'}







entry__we_want_to_edit = "IP_Cloudflare" # specifies the entry we want to edit in for loop

#iterating through specific dictionary
for key, value in MAIN_dictionary["backup_ip_dictionary"].items():
    

    # Find the exact line we want to edit
    if key == entry__we_want_to_edit: 
        print(key, value)

        MAIN_dictionary["backup_ip_dictionary"].update({key: [value[0], False] })

        print(MAIN_dictionary["backup_ip_dictionary"])




# then simply overwrite file to stores last_status.txt

    with open("test_log.txt", 'w') as file: 
        yaml.dump(MAIN_dictionary, file, sort_keys=False) 



