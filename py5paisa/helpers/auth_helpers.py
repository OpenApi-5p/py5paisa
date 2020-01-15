import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

from Crypto.Cipher import AES
from .padding import pad
import os

import base64


class EncryptionClient:

    def __init__(self):
        self.enc_key = None
        self.iv = os.urandom(16)
        self.derived_key = None
        self.cipher = None
        self.backend = default_backend()

    def _pad_and_convert_to_bytes(self, text):
        plaintext = bytes(text, encoding="utf-8")
        padded = pad(plaintext, AES.block_size, style='pkcs7')
        return padded

    def _get_enc_key(self):
        enc_key = os.getenv("ENCRYPTION_KEY")
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
        self.cipher = AES.new(self.derived_key, AES.MODE_ECB, self.iv)

    def encrypt(self, text):
        self._get_enc_key()
        self._get_derived_key()
        self.get_cipher()
        padded_text = self._pad_and_convert_to_bytes(text)
        return base64.b64encode(self.cipher.encrypt(padded_text))
