
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from server.utils.dynamo_utils import get_account_id_from_api_key

# connect to the dynamoDB

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

# get the table named user_camera_api_keys

table = dynamodb.Table('user_camera_api_keys')

# print items in the table

response = table.scan()
items = response['Items']
print(items[0]['api_key'])

print(get_account_id_from_api_key('YourCameraAPIKey'))
print(get_account_id_from_api_key(items[0]['api_key']))
# add an item to the table


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




