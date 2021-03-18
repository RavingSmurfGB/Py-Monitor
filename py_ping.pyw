import os, time
from datetime import datetime

OS_TYPE = os.name
# Sets the count modifier to the os type
COUNT = '-n' if OS_TYPE == 'nt' else '-c'

ip_list = ["127.0.0.1", "192.168.3.200", "192.168.3.1", "1.1.1.1", "Google.com"]


while True:
    for ip in ip_list:

        response = os.popen(f"ping {ip} {COUNT} 1").read()
        if "Received = 1" in response and "Approximate" in response:
            print(f"UP {ip} Ping Successful")
            with open("results.txt", "a") as file:
                dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                file.write(dt_string + f" -- UP {ip} Ping Successful" + "\n")
            

        else:
            print(f"Down {ip} Ping Unsuccessful")
            with open("results.txt", "a") as file:
                dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                file.write(dt_string + f" -- Down {ip} Ping Unsuccessful" + "\n")

        time.sleep(60)

