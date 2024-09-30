import boto3

from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta


# connect to the dynamoDB

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

def get_account_id_from_api_key(api_key: str, time_stamp: str):
    table = dynamodb.Table('user_camera_api_keys')
    response = table.query(
        KeyConditionExpression='api_key = :apikeyvalue',
        ExpressionAttributeValues={
            ':apikeyvalue': api_key
        }
    )
    items = response.get('Items', [])
    if len(items) == 0: # Item not in table
        return None
    
    if time_stamp > items[0]['time_stamp']: # If the new timestamp is greater than the timestamp in the database, its not a replay and is valid
        update_api_key_timestamp('user_camera_api_keys', api_key, items[0]['account_id'], time_stamp)
        return items[0]['account_id']

    return items



# Updates the api key entry with the most recent timestamp
def update_api_key_timestamp(table_name: str, api_key: str, account_id: str, timestamp: str):
    table = dynamodb.Table(table_name)
    response = table.update_item(
        Key={
            'api_key': api_key,
            'account_id': account_id
        },
        UpdateExpression="set time_stamp = :t",
        ExpressionAttributeValues={
            ':t': timestamp
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def store_temperature_and_humidity_in_dynamoDB(table_name: str, item: dict):
    # Dictionary Example: {'account_id':XXXXXX, 'temperature': 3.5, 'humidity': 0.5, 'timestamp': '2021-01-01T12:00:00'}
    table = dynamodb.Table(table_name)
   

    response = table.put_item(Item=item)
    return response
    
def get_latest_fridge_conditions_from_dynamoDB(table_name: str, account_id: str):
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('account_id').eq(account_id),
        ScanIndexForward=False,
        Limit=1
    )
    items = response.get('Items', [])
    return items

def get_historical_fridge_conditions_from_dynamoDB(table_name: str, account_id: str):
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('account_id').eq(account_id),
        ScanIndexForward=False,
        Limit=20
    )
    items = response.get('Items', [])
    return items

# This function checks that the timestamp included in the api key is after the most recent api key in the database
# Its passed the api_key and the timestamp and object from dynamoDB
def check_api_key_timestamp(api_key: str, timestamp: str, items: dict):
    # If the timestamp is after the most recent timestamp in the database then the timestamp is valid
    if timestamp > items[0]['timestamp']:
        return True
    return False





def store_item_in_dynamoDB(table_name: str, item: dict):
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=item)
    return response 


# Create a new food item in fridge_items table
def store_fridge_item_in_dynamoDB(table_name: str, item: dict):
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=item)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    elif response['ResponseMetadata']['HTTPStatusCode'] == 400:
        return False
    




def fetch_item_photo_url( account_id: str, item_id: str, table_name: str='fridge_items'):
    table = dynamodb.Table(table_name)
    print('account_id:', account_id)
    print('item_id:', item_id)
    try:
        response = table.get_item(
            Key={
                'account_id': account_id,
                'item_id': item_id
            }
        )
        print(response['Item'])
        if 'Item' in response: return response["Item"]["real_photo_path"]
        else: return None
    except Exception as e: return None



# This should list all items that belong to the account_id
def list_items_in_fridge(account_id: str , table_name: str='fridge_items'):
    # Use the query method to retrieve items based on the account_id partition key
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('account_id').eq(account_id)
    )
    
    # The 'Items' key in the response contains the query results
    items = response['Items']
    
   
    
    return items


# This function returns items belonging to an account ID that expire within a certain number of days
def list_items_expiring_soon(account_id: str, days: int=5, table_name: str='fridge_items'):
    # Use the query method to retrieve items based on the account_id partition key
    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('account_id').eq(account_id)
    )
    
    # The 'Items' key in the response contains the query results
    items = response['Items']
    soon_to_expire = []
    for item in items:
        if item['expiration_date']:
           
            expiration_date = datetime.strptime(item['expiration_date'], "%Y-%m-%d")
            if expiration_date <= datetime.now() + timedelta(days=days) :#and expiration_date >= datetime.now():
                soon_to_expire.append(item)
    return soon_to_expire

# This functions gets an item from the fridge_items table

def get_item_from_dynamoDB(table_name: str, account_id: str, item_id: str):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'account_id': account_id,
            'item_id': item_id
        }
    )
    return response


# This function deletes an item from the fridge_items table
def delete_item_from_dynamoDB(table_name: str, account_id: str, item_id: str):
    table = dynamodb.Table(table_name)

    item = get_item_from_dynamoDB(table_name, account_id, item_id)

    response = table.delete_item(
        Key={
            'account_id': account_id,
            'item_id': item_id
        }
    )
    return response


def update_item_in_fridge(data: dict):

    table = dynamodb.Table('fridge_items')

    update_expression = 'SET '
    expression_attribute_values = {}
    for key, value in data.items():
        if key not in ['account_id', 'item_id','timestamp']:  # Skip keys that are not attributes to update
            update_expression += f"{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value
    
    # Remove trailing comma and space
    update_expression = update_expression.rstrip(', ')
    
    try:
        # Update the item in the DynamoDB table
        response = table.update_item(
            Key={
                'account_id': data['account_id'],
                'item_id': data['item_id']
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"  # Returns the values of the attributes after the update
        )    
        return True
    except Exception as e:
        print(f"Error updating item in DynamoDB: {e}") 
        return False