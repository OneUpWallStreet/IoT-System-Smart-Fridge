#This file contains all the utility functions that the cron job uses to interact with the database and s3, and notification
import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Attr
from typing import List, Dict


# This function returns the items in the fridge that will expire tomorrow

item_table = boto3.resource('dynamodb', region_name='us-west-1').Table('fridge_items')

def get_items_expiring_tomorrow() -> List[Dict]:
    # Get the current date
    today = datetime.now()
    # Get the date for tomorrow
    tomorrow = today + timedelta(days=1)
    # Convert the date to a string
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')
    print(tomorrow_str)
    # Get all items in the fridge where the expiration date is tomorrow
    response = item_table.scan(
        FilterExpression=Attr('expiration_date').eq(tomorrow_str)
    )
    items = response.get('Items',[])
    print(len(items))
    print(items)
    return items# [{'expired': False, 'classname': 'apple', 
                 #   'item_id': 'eac6438e-d52f-11ee-92d0-936ff7aa2e83', 
                 #   'timestamp': '2024-02-26T21:20:27.226970', 
                 #   'real_photo_path': 'items/eac6438e-d52f-11ee-92d0-936ff7aa2e83.jpeg', 
                 #   'expiration_date': '2024-02-25', 'account_id': 'XXXXXX'}]

def get_items_already_expired() -> List[Dict]:
    # Get the current date
    today = datetime.now()
    # Convert the date to a string
    today_str = today.strftime('%Y-%m-%d')
    print(today_str)
    # Get all items in the fridge where the expiration date is tomorrow
    response = item_table.scan(
        FilterExpression=Attr('expiration_date').lt(today_str)
    )
    items = response.get('Items',[])
    print(len(items))
    print(items)
    return items # [{'expired': False, 'classname': 'apple', 
                 #   'item_id': 'eac6438e-d52f-11ee-92d0-936ff7aa2e83', 
                 #   'timestamp': '2024-02-26T21:20:27.226970', 
                 #   'real_photo_path': 'items/eac6438e-d52f-11ee-92d0-936ff7aa2e83.jpeg', 
                 #   'expiration_date': '2024-02-25', 'account_id': 'XXXXXX'}]

get_items_already_expired()