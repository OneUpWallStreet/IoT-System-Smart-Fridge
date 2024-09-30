
import requests

from encryption_utils import *




def get_recipe_endpoint(server_url, api_key:str):
    url = server_url + "/mobile/recipe"  # Change this to your Flask server's URL

    #headers = encrypt_api_key_header(api_key)

    headers = {
        "X-API-KEY": api_key,
        "DEVICE": "MOBILE"
    }

    response = requests.get(url, headers=headers)

    return response.json()



api_key = b'YourCameraAPIKey'

jack_server_url = "http://52.52.9.39:5000"
prod_server_url = "http://52.8.39.250:5000"
local_server_url = "http://127.0.0.1:5000"

response = get_recipe_endpoint(local_server_url, api_key)

print(response)