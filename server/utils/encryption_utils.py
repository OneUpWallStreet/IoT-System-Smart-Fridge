
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

def generate_keys():
    # Generate a new private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Get the public key
    public_key = private_key.public_key()

    # Serialize the public key to send to the camera
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Serialize the private key to save on the server
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Save the public key
    with open('keys/server_public_key_fresh.pem', 'wb') as f:
        f.write(public_key_bytes)
    
    # Save the private key
    with open('keys/server_private_key_fresh.pem', 'wb') as f:
        f.write(private_key_bytes)

# Assume this public key is sent to the camera and the camera sends back encrypted API key
# For this example, let's simulate the encryption process

# Server decrypts the API key
def decrypt_api_key(encrypted_api_key, private_key_name='keys/server_private_key_fresh.pem'):


    # Load the private key
    with open(private_key_name, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )

    return private_key.decrypt(
        encrypted_api_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


#load public key
def load_public_key(pub_key_name):
    with open(pub_key_name, 'rb') as f:  # Open the file in binary mode
        public_key = f.read()
    return public_key


# This function recieves an encoded encrypted API key and 1. decodes 2. decrypts it and returns the decrypted API key
def decode_decrypt_api_key(encoded_api_key, private_key_name='keys/server_private_key_fresh.pem'):
    decoded_api_key = base64.b64decode(encoded_api_key)
    decrypted_key = decrypt_api_key(decoded_api_key, private_key_name)
    return decrypted_key

   

# When you receive the encrypted API key from the camera, use decrypt_api_key function.
