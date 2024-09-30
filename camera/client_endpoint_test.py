import requests
from datetime import datetime
import json
from encryption_utils import encrypt_api_key_header

# from encryption_comm import get_public_key, load_public_key, send_encrypted_api_key

# Assuming 'apple.png' is in the same directory as this script


# IP addresses for the servers
#use prod for general testing

jacks_device = "http://52.52.9.39:5000"
prod_server_url = "http://52.8.39.250:5000"
local_server_url = "http://127.0.0.1:5000"

def test_upload_image(server_url):

    image_path = "apple.png"
    url = server_url + "/apikey_test"  # Change this to your Flask server's URL

    # Example attributes
    timestamp = datetime.now().isoformat()
    classname = "apple"
    unique_id = "1234567890"
    api_key = "YourCameraAPIKey"

    files = {"image": open(image_path, "rb")}
    data = {"timestamp": timestamp, "classname": classname, "unique_id": unique_id}
    headers = encrypt_api_key_header(b'YourCameraAPIKey')
    response = requests.get(url, data=data, files=files, headers=headers)

    print(response.text)


def fridge_image_upload(server_url, account_id:str, filename:str="fridge-example.png"):

    image_path = filename
    url = server_url + "/fridge/photo"  # Change this to your Flask server's URL

    # Example attributes
    timestamp = datetime.now().isoformat()
    classname = "apple"
    unique_id = "1234567890"
    #api_key = "YourCameraAPIKey"

    files = {"image": open(image_path, "rb")}
    data = {"account_id":account_id, "unique_id": unique_id}
    #headers = {"X-API-KEY": api_key}
    headers = encrypt_api_key_header(b'YourCameraAPIKey')
    response = requests.post(url, data=data, files=files, headers=headers)

    print(response.text)


def item_image_upload(server_url, account_id:str, classname:str, filename:str="fridge-example.png"):

    image_path = filename
    url = server_url + "/item/upload"  # Change this to your Flask server's URL

    # Example attributes
    timestamp = datetime.now().isoformat()
    #api_key = "YourCameraAPIKey"

    files = {"image": open(image_path, "rb")}
    data = {"classname":classname, "timestamp":timestamp}
    #headers = {"X-API-KEY": api_key}
    headers = encrypt_api_key_header(b'YourCameraAPIKey')
    response = requests.post(url, data=data, files=files, headers=headers)

    print(response.text)

def humid_temp_upload(server_url,temp:str,humid:str, api_key:str):
    url = (
        server_url + "/fridge/conditions"
    )  # Change this to your Flask server's URL
    
    # Example attributes
    timestamp = datetime.now().isoformat()

    account_id = "XXXXXX"

    data = {
        "timestamp": timestamp,
        "humidity": humid,
        "temperature": temp,
        "account_id": account_id,
    }

    json_data = json.dumps(data)

    # Set the header to indicate JSON content
    #headers = {"Content-Type": "application/json"}
    headers = encrypt_api_key_header(api_key)
    

    response = requests.post(url, data=json_data, headers=headers)
    print(response.text)


def send_encrypted_api_key_header(api_key, server_url):
    url = (
        server_url + "/encrypted_api_key_header"
    )  # Change this to your Flask server's URL

    headers = encrypt_api_key_header(api_key)

    response = requests.get(url, headers=headers)

    return response.text


#fridge_image_upload(local_server_url,account_id="XXXXXX")