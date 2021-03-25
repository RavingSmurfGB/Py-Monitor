
import subprocess, threading


def test():
    response = subprocess.getoutput("nslookup ")

    #response = subprocess.check_output("dir")
    print(str(response) + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")



thread_test = threading.Thread(target=test) # Declares the thread_vpn to the function vpn_reconnection()


thread_test.start() 