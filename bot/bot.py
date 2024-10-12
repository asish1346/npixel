import os
import threading
import asyncio
from bot.painter import painters
from bot.mineclaimer import mine_claimer
from bot.utils import Colors
from bot.notpx import NotPx
from telethon.sync import TelegramClient
from licensing.models import *
from licensing.methods import Key, Helpers

RSAPubKey = "<RSAKeyValue><Modulus>oPIn7id+tMI9eypGoTCsur/hiLHoGyz1Um1om8OjejOq5WnYlXg55JKwdIPIJQIKbJeNLBzrPs9ca7K9jxZT5+Ms9JQMCYHoxfJcghN49nR3i6FrPtzkZUrqAQKygvkyIH9P5crWJXqAkTMqVrVR56oHzPe1FfzZn64UHz/zLxONvzDT98JJj/CUwiewyxj7pRhVWz59cuHJAgXtwARxj+G2gq0l1oMTkQi2ICtrIRneqZXnZHDvOa9DIrDZUliAYeIRTEWBioTIuQq/h4O2KjEXuY8/hVP89Z7uMcTwGjPr84r9eQygp6W2csGx6tdK1CAxJUXhmy1GwvdunBNzPw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyI5NTQ3NjkzMSIsInZvWC9rZHhxZWxwZWVYWWtVSHF4WFZRUmpEVjZEM0dVREZ3dHV1cVciXQ=="
product_id = '27673'

def Authkey():
    key = input("Enter Auth Key: ")
    result = Key.activate(token=auth,
                          rsa_pub_key=RSAPubKey,
                          product_id=product_id,
                          key=key,
                          machine_code=Helpers.GetMachineCode())

    yellow = "\033[93m"
    reset = "\033[0m"

    if result[0] is None or not Helpers.IsOnRightMachine(result[0]):
        print(f"{yellow}The license does not work: {result[1]}{reset}")
        return False  # License is not valid
    else:
        print(f"{yellow}The license is valid!{reset}")
        return True  # License is valid

def process():
    print(r"""{}
   ('-.      .-')    ('-. .-.             
  ( OO ).-. ( OO ). ( OO )  /             
  / . --. /(_)---\_),--. ,--. ,--. ,--.   
  | \-.  \ /    _ | |  | |  | |  | |  |   
.-'-'  |  |\  :` `. |   .|  | |  | | .-') 
 \| |_.'  | '..`''.)|       | |  |_|( OO )
  |  .-.  |.-._)   \|  .-.  | |  | | `-' /
  |  | |  |\       /|  | |  |('  '-'(_.-' 
  `--' `--' `-----' `--' `--'  `-----'    
                                                                                                  
    Auto Paint Tool For NotPixel -Asʜᴜ || ☠️ xᴅ
    Author  : Asʜᴜ || ☠️ xᴅ
    Get Updates: https://telegram.dog/lootersera_th {}""".format(Colors.GREEN, Colors.END))

    
    if not Authkey():
        print("Exiting due to invalid license.")
        return  

    while True:
        print("\nMain Menu:")
        print("1. Add Account session")
        print("2. Start Mine + Claim")
        print("3. Add API ID and Hash")
        print("4. Reset API Credentials")
        print("5. Reset Session")
        print("6. Exit")

        option = input("Enter your choice: ")

        if option == "1":
            name = input("\nEnter Session name: ")
            if not os.path.exists("sessions"):
                os.mkdir("sessions")
            if not any(name in i for i in os.listdir("sessions/")):
                api_id, api_hash = load_api_credentials()
                if api_id and api_hash:
                    client = TelegramClient("sessions/" + name, api_id, api_hash).start()
                    client.disconnect()
                    print("[+] Session {} {}saved success{}.".format(name, Colors.GREEN, Colors.END))
                else:
                    print("[!] API credentials not found. Please add them first.")
            else:
                print("[x] Session {} {}already exists{}.".format(name, Colors.RED, Colors.END))
        elif option == "2":
            if not os.path.exists("sessions"):
                os.mkdir("sessions")
            dirs = os.listdir("sessions/")
            sessions = list(filter(lambda x: x.endswith(".session"), dirs))
            sessions = list(map(lambda x: x.split(".session")[0], sessions))

            for session_name in sessions:
                try:
                    cli = NotPx("sessions/" + session_name)

                    def run_painters():
                        asyncio.run(painters(cli, session_name))

                    def run_mine_claimer():
                        asyncio.run(mine_claimer(cli, session_name))

                    threading.Thread(target=run_painters).start()
                    threading.Thread(target=run_mine_claimer).start()
                except Exception as e:
                    print("[!] {}Error on load session{} \"{}\", error: {}".format(Colors.RED, Colors.END, session_name, e))
        elif option == "3":
            add_api_credentials()
        elif option == "4":
            reset_api_credentials()
        elif option == "5":
            reset_session()
        elif option == "6":
            print("Exiting...")
            break
        else:
            print("[!] Invalid option. Please try again.")

if __name__ == "__main__":
    if not os.path.exists("sessions"):
        os.mkdir("sessions")
    process()
