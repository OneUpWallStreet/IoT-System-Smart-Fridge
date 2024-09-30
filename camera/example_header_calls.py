
from datetime import datetime

# Assuming 'apple.png' is in the same directory as this script

from client_endpoint_test import (
    send_encrypted_api_key_header,
)


# Example API key
api_key = b"YourCameraAPIKey"  # The API key to encrypt
# Append the curruent time to the API key after a comma to make it unique


print(api_key)


# Choose server url
jack_server_url = "http://52.52.9.39:5000"
prod_server_url = "http://52.8.39.250:5000"
local_server_url = "http://127.0.0.1:5000"
# Get the public key from the server and save it to a file
# public_key_bytes = get_public_key(server_url=server_url)


#create a UUID for the account_id with type UUID
#account_id = str(uuid.uuid1())

#print(account_id)
# Send the encrypted API key to the server
response = send_encrypted_api_key_header(api_key, server_url=local_server_url)

print(response)
