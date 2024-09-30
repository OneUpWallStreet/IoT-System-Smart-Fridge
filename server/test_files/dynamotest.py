
# this file is used to test the dynamoDB table named "fridge_list" 

import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# connect to the dynamoDB

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

# get the table named "fridge_list"

table = dynamodb.Table('fridge_list')

# print items in the table

response = table.scan()
items = response['Items']
print(items)

# add an item to the table

table.put_item(
    Item={
        'account_id': '101011',
        'date': '2024-2-13',
        'item_quantity': 10
    }
)

# This should list all items that belong to the account_id
# 
def list_items_in_fridge(account_id: str):
    # Use the query method to retrieve items based on the account_id partition key
    response = table.query(
        KeyConditionExpression=Key('account_id').eq(account_id)
    )
    
    # The 'Items' key in the response contains the query results
    items = response['Items']
    
    # You can process the items as needed, here we're just printing them
    for item in items:
        print(json.dumps(item, indent=4))




response = table.scan()
items = response['Items']
print(items)