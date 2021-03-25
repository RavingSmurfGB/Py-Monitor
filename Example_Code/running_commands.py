
import subprocess

#This is an example of how to run a command and get a string decoded output


def run_actual_command(command):
#This code will run any command it is given, then convert it to a decoded string

#variables used:
#   new_response -- declares an emtpy string, then used to add each decoded line together
#   reponse -- refrences the command ran
    new_response = ""
    response = subprocess.Popen(command, stdout=subprocess.PIPE) #Performs the route print command and set's it to equal resonse
    
    for line in iter(response.stdout.readline, b''): # iterates through each line of the response and does bellow
        line = line.decode("utf-8") # Decodes the result in to utf-8 and converts to string
        
        new_response = new_response + line

    return new_response

command = "nslookup googleasdas.com"

output = run_actual_command(command)

print(output)