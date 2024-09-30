
#Tests the item/photo upload endpoint


import requests
from datetime import datetime
import json
from encryption_utils import *



# Example API key
  # The API key to encrypt




def upload_item(server_url, api_key:str, image_path:str, classname:str):

    #image_path = "apple.png"
    url = server_url + "/item/upload"  # Change this to your Flask server's URL

    #Header with encrypted API key
    headers = encrypt_api_key_header(api_key)

    # Example attributes
    
    timestamp = datetime.now().isoformat()

    files = {"image": open(image_path, "rb")}
    data = {"classname": classname, 'timestamp':timestamp}

    response = requests.post(url, data=data, files=files, headers=headers)

    return response.json()


'''

api_key = b'YourCameraAPIKey'

jack_server_url = "http://52.52.9.39:5000"
prod_server_url = "http://52.8.39.250:5000"
local_server_url = "http://127.0.0.1:5000"

upload_item(local_server_url, api_key, "apple.png", "apple")
'''