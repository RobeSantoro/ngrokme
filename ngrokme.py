"""
1. Query the ngrok API for the public URL of a TCP tunnel
$ ngrok api endpoints list

2. Start a RDP session to the public URL of the TCP tunnel execute
$ Start-Process "$env:windir\system32\mstsc.exe" -ArgumentList "/v:<public URL>"
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
        print(Fore.RED + 'ERROR: Check ngrok configuration.')
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

    # Start a RDP session to the public URL
    powershell_cmd = f'Start-Process "$env:windir\system32\mstsc.exe" -ArgumentList "/v:{ public_url }"'

    # Execute the PowerShell command
    subprocess.run(["powershell", "-Command", powershell_cmd])


if __name__ == '__main__':
    ngrokme()
