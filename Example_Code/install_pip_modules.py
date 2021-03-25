import subprocess, sys

with open("requirements.txt") as file: 
    for line in file:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', line])




