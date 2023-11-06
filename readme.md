# **Ngrokme**

## **Description**

Ngrokme is a simple script that allows you to obtain the TCP address of a Ngrok tunnel endpoint and start a Windows Remote Desktop Connection to that endpoint.  

This can be useful for quickly and easily accessing a remote Windows machine via a Ngrok tunnel with a **free Ngrok account** that changes the TCP address every time the remote machine is restarted.

## Requirements

- Windows: Ensure that the Windows Remote Desktop Connection client is installed on your system
- Ngrok: Ensure that Ngrok is installed and configured on your system and that there is an active Ngrok tunnel on the remote Windows machine.

## **How to Use**

1. Create a Ngrok API token:

   - Visit the Ngrok website at [ngrok.com](https://ngrok.com/) and sign in to your account.
   - In your Ngrok dashboard, navigate to the "API" section to create an API token.
   - Copy the generated API token as you'll need it in the next step.

2. Configure Ngrok with your API token:

   - Open a terminal or command prompt.
   - Run the following command to add your Ngrok API token to the configuration:

   ```bash
   ngrok config add-api-key "{YOUR_API_KEY}"
   ```

   Replace `{YOUR_API_KEY}` with the API token you generated in step 1.

3. Download the Ngrokme executable from the [Releases](https://github.com/robesantoro/ngrokme/releases) section of this repository.

4. Place the Ngrokme executable in a convenient location on your system and launch it.

The script will query the Ngrok API to obtain the public URL of a TCP tunnel endpoint and then start a Remote Desktop Connection to that endpoint.

1. You will be prompted to log in to the remote Windows machine.

## **Important Notes**

- Make sure your Ngrok tunnel is up and running before executing this script.
- You might be prompted for authentication when connecting to the remote Windows machine.

## **Disclaimer**

- This script is intended for educational and testing purposes only.
- Ensure that you have permission to access the remote machine via Ngrok.

Please use this script responsibly and in compliance with any applicable laws and regulations.