

import requests
from datetime import datetime

from encryption_utils import *





def get_fridge_items(server_url, api_key:str):
    url = server_url + "/fridge/items"  # Change this to your Flask server's URL

    headers = encrypt_api_key_header(api_key)

    response = requests.get(url, headers=headers)

    #print(response.text)
    return response.json()




'''
api_key = b'YourCameraAPIKey'

jack_server_url = "http://52.52.9.39:5000"
prod_server_url = "http://52.8.39.250:5000"
local_server_url = "http://127.0.0.1:5000"

response = get_fridge_items(local_server_url, api_key)

print(response[0])'''

