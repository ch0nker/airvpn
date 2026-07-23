from __future__ import annotations

from airvpn.exceptions import RSAError, AESEncryptionError, AESDecryptionError, RCParseError, LoginError
from airvpn.client.models import *

from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA


import platform
import requests
import random
import base64
import os
import re

class AirClient:
    """
    A client for interacting with the AirVPN API. This class handles various tasks such as parsing configuration files,
    encrypting parameters, making requests to the API, and decrypting responses. It supports operations like logging in,
    retrieving manifest information, and handling RSA and AES encryption.
    
    Attributes:
        RC_URL (str): The URL of the AirVPN configuration file.
    """
    RC_URL = "https://gitlab.com/AirVPN/AirVPN-Suite/-/raw/master/AirVPN-Suite/etc/airvpn/bluetit.rc?ref_type=heads"

    def __init__(self):
        """
        Initialize the AirClient with a session for making HTTP requests.
        """
        self.session = requests.Session()

    def parse_rc(self) -> dict[str, str | list[str]]:
        """
        Parse the configuration file from the specified URL and return a dictionary of key-value pairs.

        Returns:
            dict[str, str | list[str]]: A dictionary containing configuration parameters.
        """
        text = requests.get(AirClient.RC_URL).text
        result = {}

        matches = re.findall(r"^(?!#)(\w+)\s+(.+)$", text, re.MULTILINE)
        for key, value in matches:
            if result.get(key):
                if isinstance(result[key], list):
                    result[key].append(value)
                    continue
                value = [result[key], value]

            result[key] = value

        return result

    def system_description(self) -> str:
        """
        Determine the description of the current system.

        Returns:
            str: The description of the current system.
        """
        return platform.system()

    def architecture(self) -> str:
        """
        Determine the architecture of the current system.

        Returns:
            str: The architecture of the current system.
        """
        return platform.machine()

    def b64_map(self, params: dict) -> str:
        """
        Encode a dictionary of parameters into a base64 string.

        Args:
            params (dict): A dictionary containing the parameters to encode.

        Returns:
            str: The encoded base64 string.
        """
        output = ""
        for key, value in params.items():
            output += base64.b64encode(str(key).encode()).decode()
            output += ":"
            output += base64.b64encode(value if isinstance(value, bytes) else str(value).encode()).decode()
            output += "\n"
        return output

    def decrypt_response(self, response_content: bytes, secret_key: bytes, iv: bytes) -> str:
        """
        Decrypt the AES-encrypted response content using the provided secret key and IV.

        Args:
            response_content (bytes): The encrypted response content.
            secret_key (bytes): The secret key used for decryption.
            iv (bytes): The initialization vector used for decryption.

        Returns:
            str: The decrypted plaintext string.

        Raises:
            AESDecryptionError: If an error occurs during the decryption process.
        """
        aes_decryptor = AES.new(secret_key, AES.MODE_CBC, iv)
        decrypted_padded = aes_decryptor.decrypt(response_content)
        try:
            decrypted = unpad(decrypted_padded, AES.block_size)
        except ValueError as e:
            raise AESDecryptionError(f"AES decryption error: {e}") from e
        return decrypted.decode()

    def build_encrypted_params(self,
        rsa_modulus_b64: str,
        rsa_exponent_b64: str,
        params: dict,
        key_size: int = 32,
        iv_size: int = 16
    ) -> tuple[bytes, bytes, bytes, bytes]:
        """
        Encrypt the parameters using RSA and AES encryption.

        Args:
            rsa_modulus_b64 (str): The base64-encoded modulus of the RSA public key.
            rsa_exponent_b64 (str): The base64-encoded exponent of the RSA public key.
            params (dict): A dictionary containing the parameters to encrypt.
            key_size (int, optional): The size of the secret key in bytes. Defaults to 32.
            iv_size (int, optional): The size of the initialization vector in bytes. Defaults to 16.

        Returns:
            tuple[bytes, bytes, bytes, bytes]: A tuple containing the encrypted association parameters,
                                                encrypted data parameters, secret key, and IV.

        Raises:
            RSAError: If an error occurs during RSA encryption.
            AESEncryptionError: If an error occurs during AES encryption.
        """
        rsa_mod_int = int.from_bytes(base64.b64decode(rsa_modulus_b64), byteorder="big")
        rsa_exp_int = int.from_bytes(base64.b64decode(rsa_exponent_b64), byteorder="big")

        rsa_public_key = RSA.construct((rsa_mod_int, rsa_exp_int))

        secret_key = os.urandom(key_size)
        iv = os.urandom(iv_size)

        assoc_param_s = self.b64_map({
            "key": secret_key,
            "iv": iv
        })

        rsa_cipher = PKCS1_v1_5.new(rsa_public_key)
        try:
            bytes_param_s = rsa_cipher.encrypt(assoc_param_s.encode())
        except (ValueError, TypeError) as e:
            raise RSAError(f"RSA error: {e}") from e

        aes_data_in = self.b64_map(params)

        aes_encryptor = AES.new(secret_key, AES.MODE_CBC, iv)
        try:
            padded = pad(aes_data_in.encode(), AES.block_size)
            bytes_param_d = aes_encryptor.encrypt(padded)
        except (ValueError, TypeError) as e:
            raise AESEncryptionError(f"AES encryption error: {e}") from e

        return bytes_param_s, bytes_param_d, secret_key, iv

    def request(self, action: str, **kwargs):
        """
        Make a request to the AirVPN API with the specified action and parameters.

        Args:
            action (str): The API action to perform.
            **kwargs: Additional keyword arguments representing the parameters for the API call.

        Returns:
            ElementTree.Element: An XML element tree of the decrypted response content.

        Raises:
            RCParseError: If an error occurs while parsing the RC configuration file.
            RSAError or AESEncryptionError: If an error occurs during encryption.
            AESDecryptionError: If an error occurs during decryption.
        """
        rc = self.parse_rc()

        params = {"act": action, **kwargs}

        params.setdefault("system", self.system_description())
        params.setdefault("version", "295")
        params.setdefault("software", f"python_{platform.python_version()}")
        params.setdefault("arch", self.architecture())

        bootstrap_servers = rc.get("bootserver", [])
        random.shuffle(bootstrap_servers)

        rsaexponent = rc.get("rsaexponent")
        if rsaexponent is None:
            raise RCParseError("Failed to get rsaexponent")

        rsamodulus = rc.get("rsamodulus")
        if rsamodulus is None:
            raise RCParseError("Failed to get rsamodulus")

        try:
            bytes_param_s, bytes_param_d, secret_key, iv = self.build_encrypted_params(rsamodulus, rsaexponent, params)
        except (RSAError, AESEncryptionError) as e:
            raise AESEncryptionError(f"Encryption failed: {e}")

        encrypted_params = {
            "s": base64.b64encode(bytes_param_s).decode(),
            "d": base64.b64encode(bytes_param_d).decode(),
        }

        for url in bootstrap_servers:
            response = requests.post(url,
                                    headers={
                                        "Accept": "",
                                        "Content-Type": "application/x-www-form-urlencoded"},
                                    data=encrypted_params, timeout=10)

            if response.status_code == 200 and response.content is not None:
                try:
                    return self.decrypt_response(response.content, secret_key, iv)
                except (ValueError, TypeError) as e:
                    raise AESDecryptionError(f"AES decryption error: {e}")

    def login(self, username: str, password: str):
        """
        Authenticate with the AirVPN API using the provided username and password.

        Args:
            username (str): The username to use for authentication.
            password (str): The password to use for authentication.

        Returns:
            User: A class built off the XML response.

        Raises:
            LoginError: If the login's `message_action` is stop.
        """
        user = User.from_string(self.request("user", login=username, password=password))

        if user.message_action == "stop":
            raise LoginError(user.message)

        return user

    def manifest(self):
        """
        Retrieve the manifest information from the AirVPN API.

        Returns:
            Manifest: A class built off the XML response.
        """
        return Manifest.from_string(self.request("manifest"))
