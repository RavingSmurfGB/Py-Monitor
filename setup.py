import os, shutil, pathlib, ctypes, sys, subprocess, stat, subprocess, time


current_file_path = pathlib.Path(__file__).parent.absolute() #This will get the current file path but will not update if you move the setup.py, move the setup.py last 
print(current_file_path)

#-1. Relaunch program as admin if not:                          Done (with error)
#0. Install pip requirements!!!                                 Done

#1. Move files to setup at launch:                              Done
#2. Move files to start menu:                                   Done
#3. Move all files to program files in permanent location       Done
#4. Launch program                                              Not started

#*. Perhaps work on gui showing what is happening
#*. Recreate the shortcuts under programfiles...
#*. If already installed perhaps delete and reinstall


shortcut_name = "Py_Monitor.lnk" # Specify the shortcut link for the program e.g. "Py_Monitor.lnk"
directory_of_shortcut = "Setup_Files" # Specify under which directory the shortcut link can be found e.g. "Setup_Files"
# Example file path for the above would be (current_dir)\Setup_Files\Py_Monitor.lnk

reinstall = False




#-1.#////////////////////////////////Admin Check///////////////////////////////
#Is ran to determine if the program was started with admin rights, if so continues, if not uac prompt 

###DOES NOT WORK..................................................................................................................................
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # Code of your program here
    print("Setup already initialised with Administrator rights")
else:
    # Re-run the program with admin rights
    print("Setup was not started with Administrator rights, restarting...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


print("\n")



#0.#////////////////////////////////Installing Pip Requirements///////////////////////////////
with open("requirements.txt") as file: # Opens requirements.txt
    for line in file: # reads file line by line
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', line]) # executes pip install with each line in file

time.sleep(3)

print("\n")



#1.#////////////////////////////////Setting launch at Startup///////////////////////////////
print("Setting program to start on boot")

#Get's current username
username = os.getlogin()



dst_launch_startup_path = ("C:\\Users\\" + username + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup") #Creates the path to startup, including the current user.
src_launch_startup_path = current_file_path.joinpath(directory_of_shortcut) #Adds support_files\startup to the current file path

check_dst = dst_launch_startup_path + "\\" + shortcut_name #Creates a full file path to startup file, to check if it exists already

def startup_copy(): # Defines fucntion to copy seutp file, used later in logic
    file_names = pathlib.Path.iterdir(src_launch_startup_path)
    try:
        for file_name in file_names:
            shutil.copy(pathlib.PurePath.joinpath(src_launch_startup_path, file_name), dst_launch_startup_path)
    except:
        print("Warning: Something went wrong during moving startup file... \n" + "Double check that file exists under \n" + check_dst)


if pathlib.Path(check_dst).is_file() == False:
    # If there isnt a file in starup then:
    print("Moving file to startup")
    startup_copy()
elif pathlib.Path(check_dst).is_file() == True:
    #If there is a file in startup then:
    if reinstall == False:
        print("ERROR: Startup file already exsists under : \n" + "   " + check_dst + "\n Please select reinstall from the menu if you would like to continue")
    if reinstall == True:
        #insert code to delete file here
        print("not yet implemented")

#///////////////////////////////


print("\n")

#2.#////////////////////////////////Adding to start menu///////////////////////////////




dst_launch_startup_path = ("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs") #Creates the path to startup, including the current user.
src_launch_startup_path = current_file_path.joinpath(directory_of_shortcut) #Adds support_files\startup to the current file path


check_dst = dst_launch_startup_path + "\\" + shortcut_name #Creates a full file path to startup file, to check if it exists already


def start_menu_copy():
    try:
        file_names = pathlib.Path.iterdir(src_launch_startup_path)
        for file_name in file_names:
            shutil.copy(pathlib.PurePath.joinpath(src_launch_startup_path, file_name), dst_launch_startup_path)
    except:
        print("Warning: Something went wrong during moving start menu file... \n" + "Double check that file exists under \n" + check_dst)

if pathlib.Path(check_dst).is_file() == False:
    print("Moving file to start_menu")
    start_menu_copy()
elif pathlib.Path(check_dst).is_file() == True:
    #If there is a file in startup then:
    if reinstall == False:
        print("ERROR: Start Menu file already exsists under : \n" + "   " + check_dst + "\n Please select reinstall from the menu if you would like to continue")
    if reinstall == True:
        #insert code to delete file here
        print("not yet implemented")



#///////////////////////////////




print("\n")


#3. ////////////////////////////////Moving Main Files///////////////////////////////

source_dir = current_file_path
target_dir = 'C:\\Program Files\\Py_Monitor\\' #actual destinatiommmn C:\Program Files 


def on_rm_error(func, path, exc_info):
    #from: https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)




def move_main_files():
    source_dir = current_file_path
    try:
        for i in os.listdir(source_dir):
            if i.endswith('.git'):
                tmp = os.path.join(source_dir, i)
                # We want to unhide the .git folder before unlinking it.
                while True:
                    subprocess.call(['attrib', '-H', tmp])
                    break
                shutil.rmtree(tmp, onerror=on_rm_error)

        source_dir = current_file_path
        file_names = os.listdir(source_dir)

        for file_name in file_names:
            if pathlib.Path(target_dir).is_dir() == False:
                pathlib.Path(target_dir).mkdir()
            shutil.move(os.path.join(source_dir, file_name), target_dir)
    except:
        print("Warning: Something went wrong during moving main files... \n" + "Double check that files exists under \n" + target_dir)


if pathlib.Path(target_dir).is_dir() == False:
    print("Moving main files")
    move_main_files()
elif pathlib.Path(target_dir).is_dir() == True:
    #If there is a file in startup then:
    if reinstall == False:
        print("ERROR: Main files already exsists under : \n" + "   " +  "\n Please select reinstall from the menu if you would like to continue")
    if reinstall == True:
        #insert code to delete file here
        print("not yet implemented")
#///////////////////////////////




'''
#3. ////////////////////////////////Moving Main Files///////////////////////////////
print("Starting Program")


file = 'C:\\Program Files\\Py_Monitor\\Support_Files\\relaunch.vbs'
subprocess.call([file])

#subprocess.Popen(' """C:\Program Files\Py_Monitor\Support_Files\relaunch.vbs""" ') #str() is needed to convert the windows_path to a string for subproccess

#subprocess.call(['"C:\\Program Files\\Py_Monitor\\Support_Files\\relaunch.vbs"'])

input("Press Enter to continue...") # Makes the user hit enter to conitnue
exit()
#///////////////////////////////
'''