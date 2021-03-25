import subprocess, time

file = 'C:\\Program Files\\Py_Monitor\\Support_Files\\relaunch.vbs'
#subprocess.Popen(['WScript',file], shell=True)




subprocess.call(['WScript.exe', file], shell=True)
