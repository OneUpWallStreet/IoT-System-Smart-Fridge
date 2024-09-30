import requests
from datetime import datetime
import base64
import json

# Assuming 'apple.png' is in the same directory as this script

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from typing import Dict

# Simulate loading the public key received from the server


def get_public_key(server_url):
    url = server_url + "/public_key"
    response = requests.get(url)
    # save the public key to a file
    with open("server_public_key.pem", "wb") as file:
        file.write(response.content)

    return response.content


def load_public_key() -> bytes:
    with open("server_public_key.pem", "rb") as file:
        public_key_bytes = file.read()
    return public_key_bytes


def encrypt_api_key_header(api_key: str) -> Dict:
    public_key_bytes = load_public_key()
    public_key = serialization.load_pem_public_key(
        public_key_bytes, backend=default_backend()
    )
    api_key = api_key + b"," + str(datetime.now().timestamp()).encode("utf-8")
    # Encrypt the API key
    encrypted_api_key = public_key.encrypt(
        api_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    encoded_api_key = base64.b64encode(encrypted_api_key).decode("ascii")

    headers = {
        #"Content-Type": "application/json",
        "X-API-KEY": encoded_api_key,
        "DEVICE": "CAMERA"
    }

    return headers
