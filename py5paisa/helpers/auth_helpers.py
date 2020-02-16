import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

from Crypto.Cipher import AES
from .padding import pad
import os

import base64

from conf import encryption_key


class EncryptionClient:

    def __init__(self):
        self.enc_key = None
        self.iv = bytes([83, 71, 26, 58, 54, 35, 22, 11,
                         83, 71, 26, 58, 54, 35, 22, 11])
        self.derived_key = None
        self.cipher = None
        self.backend = default_backend()

    def _pad_and_convert_to_bytes(self, text):
        plaintext = bytes(text, encoding="utf-8")
        padded = pad(plaintext, AES.block_size, style='pkcs7')
        return padded

    def _get_enc_key(self):
        enc_key = encryption_key
        if not enc_key:
            raise Exception("ENCRYPTION_KEY not set in environment variables")
        self.enc_key = base64.b64encode(
            bytes(enc_key, encoding="utf-8"))

    def _get_derived_key(self):
        self.derived_key = PBKDF2HMAC(
            algorithm=hashes.SHA1,
            length=32,
            salt=self.iv,
            iterations=1000,
            backend=self.backend).derive(self.enc_key)

    def get_cipher(self):
        self.cipher = AES.new(self.derived_key, AES.MODE_CBC, self.iv)

    def encrypt(self, text):
        self._get_enc_key()
        self._get_derived_key()
        self.get_cipher()
        padded_text = self._pad_and_convert_to_bytes(text)
        return base64.b64encode(self.cipher.encrypt(padded_text))


def get_cookie():
    cookie = {'5paisacookie': os.getenv("COOKIE")}
    if not cookie:
        raise Exception("Invalid Session or session expired!")
    return cookie


def get_client_code():
    client_code = os.getenv("CLIENT_CODE")
    if not client_code:
        raise Exception("Not logged in!")
    return client_code
