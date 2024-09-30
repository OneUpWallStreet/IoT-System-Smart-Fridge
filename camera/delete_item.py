
import requests
from datetime import datetime

from encryption_utils import *
from get_items import get_fridge_items





def delete_fridge_item(server_url, api_key:str, item_id:str):
    url = server_url + f"/item/{item_id}"  # Change this to your Flask server's URL

    headers = encrypt_api_key_header(api_key)

    response = requests.delete(url, headers=headers)

   
    return response




'''
api_key = b'YourCameraAPIKey'

jack_server_url = "http://52.52.9.39:5000"
prod_server_url = "http://52.8.39.250:5000"
local_server_url = "http://127.0.0.1:5000"

#response = get_fridge_items(local_server_url, api_key)
#print("delete item list items before",response)
response = delete_fridge_item(local_server_url, api_key,'3905e2f0-d2b2-11ee-92d0-936ff7aa2e83')
print(response.text)

#response = get_fridge_items(local_server_url, api_key)
#print("delete item list items after",response)

'''