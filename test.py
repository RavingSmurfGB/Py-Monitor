import subprocess, os


#3. ////////////////////////////////Moving Main Files///////////////////////////////
print("Starting Program")

#subprocess.Popen(r"C:\\Program Files\\Py_Monitor\\Support_Files\\relaunch.vbs" ) #str() is needed to convert the windows_path to a string for subproccess

#subprocess.call(['"C:\\Program Files\\Py_Monitor\\Support_Files\\relaunch.vbs"'])


subprocess.Popen(['start', """C:\\Program Files\\Py_Monitor\\Support_Files\\relaunch.vbs"""])



#///////////////////////////////
#subprocess.Popen(['start', '"C:\\Folder\\This File"'], shell=True)




'''cmd = [r"C:\Program Files\Py_Monitor\Support_Files\relaunch.vbs"]
process = subprocess.Popen(cmd, shell=True )
input("Press Enter to continue...") # Makes the user hit enter to conitnue
exit()'''