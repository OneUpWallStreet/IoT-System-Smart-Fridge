
from utils.dynamo_utils import delete_item_from_dynamoDB, get_item_from_dynamoDB, fetch_item_photo_url, store_item_in_dynamoDB
from utils.s3_utils import delete_object_from_s3, put_object_in_s3, get_presigned_url
import uuid
from datetime import datetime, timedelta
from flask import jsonify




# This Function adds an item to the fridge_items table and uploads the photo to s3

def add_item_to_s3_dynamoDB(image, account_id: str, classname: str, timestamp:str):

    item_id = str(uuid.uuid1())  # Generate a unique ID for the item
    item_dict = {
            'account_id': account_id,
            'item_id': item_id,
            'classname': classname,
            'timestamp': timestamp,
            'expiration_date': None,  # Example of a default value
            'expired': False,  # Example of a default value
            'real_photo_path' : f'items/{item_id}.jpeg',
    }
    item_dict['expiration_date'] = get_expiration(item_dict)
    response = store_item_in_dynamoDB('fridge_items', item_dict)
    if response:
        print("Item uploaded successfully")
    else:
        return jsonify({"error":'Error uploading item'}), 500
    # Example of modifying the save path to include the unique_id
    save_path = f'uploads/{item_dict["real_photo_path"]}'
    image.save(save_path)
    
    data = open(f'uploads/{item_dict["real_photo_path"]}', 'rb')
    put_object_in_s3('fridgepictures', item_dict['real_photo_path'], data)
        
    return jsonify({'message': 'Item and Image uploaded successfully','item':item_dict}), 200




#this deletes an item from dynamoDB and s3

def delete_item_from_s3_dynamoDB(account_id: str, item_id: str):
    #get item
    item = get_item_from_dynamoDB('fridge_items', account_id, item_id)
    
    
    if not item.get('Item', None):
        print(f'Item not found: {item_id}')
        return False
    
    s3_object_name = item['Item']['real_photo_path']


    #delete item from dynamoDB
    response = delete_item_from_dynamoDB('fridge_items', account_id, item_id)
    if response:
        print("Item deleted from dynamoDB")
    else:
        print("Error deleting item from dynamoDB")

    #delete item from s3
    
    
    delete_object_from_s3('fridgepictures', s3_object_name)
    print(f'Item deleted: {item_id}')
    return True


# This function updates a value in the fridge_items table
#TODO: test this function

def update_item_in_dynamoDB(account_id: str, item_id: str, attribute: str, value: str):
    # Get the item from the database
    item = get_item_from_dynamoDB('fridge_items', account_id, item_id)
    if not item.get('Item', None):
        return False
    # Update the attribute
    item['Item'][attribute] = value
    # Store the updated item in the database
    response = store_item_in_dynamoDB('fridge_items', item['Item'])
    if response:
        return True
    else:
        return False
    


def get_item_photo_from_s3(account_id: str, item_id: str,table_name: str='fridge_items'):
    

    photo_path = fetch_item_photo_url(account_id, item_id)
    if photo_path:
        return get_presigned_url('fridgepictures', photo_path)
    else:
        return None




#get expiration date of item
def get_expiration(item_obj):
  #current date
  timestamp = datetime.now()
  expiry_days = {
        'apple': 7,
        'banana': 5,  # Assuming ripe bananas are stored
        'berries': 2,
        'grapes': 2,
        'watermelon': 3,
        'broccoli': 2,
        'peach': 5,
        'orange': 14,
        'lettuce': 5,
        'cauliflower': 10,
        'brussels_sprouts': 10,
        'bell_peppers': 10,
        'cucumbers': 10,
        'carrots': 16,
        'beef': 5,  # Assuming beef is stored properly immediately
        'chicken': 5,  # Assuming chicken is stored properly immediately
        'milk': 7,  # Assuming milk is stored properly immediately
        'eggs': 30,
    }
  
  classname = item_obj['classname']
  classname = classname.lower()
  if classname in expiry_days:
    # Get expiry days for the item from expiry_days dictionary
    expiry_days_count = expiry_days[classname]
    # Calculate expiry date by adding expiry days to the current date
    expiry_date = timestamp + timedelta(days=expiry_days_count)
    # Update the item with expiry_date
    return expiry_date.date().isoformat()
  else:
    # If classname not found in expiry_days, set expiry_date to None
    return None
  




# This function checks the date of the expired items and marks them as expired