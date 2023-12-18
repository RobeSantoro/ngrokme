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

from colorama import Fore, init
init(autoreset=True)


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
        print(f'Run {Fore.CYAN}ngrok config edit{Fore.RESET} to check the configuration file.')
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

    print(f'Public URL: {Fore.CYAN + public_url} ')
    print(f'{Fore.GREEN}Starting RDP session...')
    input('Press Enter to connect')

    # (Windows)
    powershell_cmd = f'Start-Process "$env:windir\\system32\\mstsc.exe" -ArgumentList "/v:{ public_url }"'

    # (MAC OSX)
    # Get the folder where the script is running
    script_dir = os.path.dirname(os.path.realpath(__file__))

    print(script_dir)

    with open(f'{script_dir}/template.rdp', 'r') as f:
        data = f.read().replace('{RDP_ADDRESS}', public_url)
    with open(f'{script_dir}/template.rdp', 'w') as f:
        f.write(data)

    # Open the .rdp file
    term_cmd = 'open template.rdp'

    if os.name == 'posix':
        # Execute the terminal command
        subprocess.run(term_cmd, shell=True)
    else:
        # Execute the PowerShell command
        subprocess.run(["powershell", "-Command", powershell_cmd])

if __name__ == '__main__':
    ngrokme()
