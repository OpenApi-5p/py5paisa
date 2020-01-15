import base64
import os
from helpers.auth_helpers import EncryptionClient


class LoginClient:

    def __init__(self, email=None, passwd=None, dob=None):
        self.email = None
        self.passwd = None
        self.dob = None

    def login(self):
        """
        TODO:
         - Understand encryption logic and make changes(if any)
         - Complete authentication.
        """
        encryption_client = EncryptionClient()
        secret_email = encryption_client.encrypt(self.email)
        secret_passwd = encryption_client.encrypt(self.passwd)
        secret_dob = encryption_client.encrypt(self.dob)
        pass
