"""
1. Query the ngrok API for the public URL of a TCP tunnel
$ ngrok api endpoints list

2. Start a RDP session to the public URL of the TCP tunnel execute
$ Start-Process "$env:windir\\system32\\mstsc.exe" -ArgumentList "/v:<public URL>"

On MAC OSX you cannot use the Microsoft Remote Desktop app from the command line.
So I created an .rdp template file in which I replace the public URL of the TCP tunnel
and open it from the terminal.
"""

import os
import json
import subprocess

from pprint import pprint
from dotenv import load_dotenv

from colorama import Fore, init
init(autoreset=True)

# Get the folder where the script is running
script_dir = os.path.dirname(os.path.realpath(__file__))
print(script_dir)

load_dotenv(f'{script_dir}/.env')

print(os.getenv('RDP_USER'))
print(os.getenv('RDP_PASSWORD'))


def ngrokme():

    # Query the ngrok API via command line
    cmd = 'ngrok api endpoints list'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()

    # Parse the JSON output if any
    try:
        data = json.loads(output)
    except json.decoder.JSONDecodeError:
        print()
        print(Fore.RED + 'ERROR: Check ngrok configuration, firewall and network settings.')
        print(f'Run {Fore.CYAN}ngrok config edit{
              Fore.RESET} to check the configuration file.')
        print()
        input('Press Enter to exit...')
        os._exit(1)

    # Get the public URL of the TCP tunnel if any
    try:
        public_url = data['endpoints'][0]['public_url'][6:]
    except IndexError:
        print()
        print(Fore.RED + 'ERROR:  No ngrok tunnel found. \nPlease check if ngrok has an active tunnel on the remote machine.')
        print()
        input('Press Enter to exit...')
        os._exit(1)

    # (MAC OSX)
    if os.name == 'posix':

        # Check if the Microsoft Remote Desktop app is installed
        if not os.path.exists('/Applications/Microsoft Remote Desktop.app'):
            print()
            print(Fore.RED + 'ERROR: Microsoft Remote Desktop app not found.')
            input('Press Enter to exit...')
            os._exit(1)

        # Check if the Microsoft Remote Desktop app is running and start it if not
        if not os.system('pgrep -x "Microsoft Remote Desktop"'):
            print()
            print(Fore.YELLOW + 'Microsoft Remote Desktop app not running. Starting it...')
            # input('Press Enter to start it...')
            os.system('open -a "Microsoft Remote Desktop"')

        with open(f'{script_dir}/template.rdp', 'r') as template_file:

            # Replace the placeholder with the current public URL
            data = template_file.read().replace('{RDP_ADDRESS}', public_url)

            # Replace the username with the user from .env fileù
            data = data.replace('{RDP_USER}', os.getenv('RDP_USER'))
            data = data.replace('{RDP_PASSWORD}', os.getenv('RDP_PASSWORD'))

            with open(f'{script_dir}/current.rdp', 'w') as current_file:
                print(data)
                current_file.write(data)

            # Close the files
            current_file.close()

        template_file.close()

        # Open the .rdp file
        term_cmd = f'open {script_dir}/current.rdp'

        # Execute the terminal command
        subprocess.run(term_cmd, shell=True)

    # (WINDOWS)
    else:
        powershell_cmd = f'Start-Process "$env:windir\\system32\\mstsc.exe" -ArgumentList "/v:{
            public_url}"'

        # Execute the PowerShell command
        subprocess.run(["powershell", "-Command", powershell_cmd])


if __name__ == '__main__':
    ngrokme()
