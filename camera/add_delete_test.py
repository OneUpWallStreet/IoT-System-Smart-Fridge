
from delete_item import delete_fridge_item
from get_items import get_fridge_items
from item_upload import upload_item
import json




api_key = b'YourCameraAPIKey'

jack_server_url = "http://52.52.9.39:5000"
prod_server_url = "http://52.8.39.250:5000"
local_server_url = "http://127.0.0.1:5000"


def add_delete_ten():
    example_fruit = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon"]

    added_items = []

    for i in range(10):
        added_items.append(upload_item(local_server_url, api_key, "photos/apple.png", example_fruit[i]))

    print("Added items", added_items)
    print()
    items_in = get_fridge_items(local_server_url, api_key)

    print("List items", items_in)
    print()
    for i in range(len(items_in)):
        response = delete_fridge_item(local_server_url, api_key, items_in[i]['item_id'])
        
        
    response = get_fridge_items(local_server_url, api_key)
    print("Items after delete", response)


def delete_all():
    items_in = get_fridge_items(local_server_url, api_key)
    for i in range(len(items_in)):
        response = delete_fridge_item(local_server_url, api_key, items_in[i]['item_id'])
    response = get_fridge_items(local_server_url, api_key)
    print("Items after delete", response)

def add_ten():
    example_fruit = ["apple", "banana", "berries", "grapes", "orange", "beef", "milk", "bell_peppers","carrots","bell_peppers","carrots"]

    added_items = []

    for i in range(10):
        added_items.append(upload_item(local_server_url, api_key, "photos/apple.png", example_fruit[i]))

    #print("Added items", added_items)
    print()
    items_in = get_fridge_items(local_server_url, api_key)

    print(json.dumps(items_in, indent=4))
    print()


add_ten()