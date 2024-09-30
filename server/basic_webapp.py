
# below is the boilerplate code for a basic webapp using Flask

from flask import Flask, request, jsonify, render_template
import base64
from functools import wraps
from utils.encryption_utils import decrypt_api_key, load_public_key, decode_decrypt_api_key
from utils.dynamo_utils import *
from decimal import Decimal
from utils.s3_utils import *
import uuid
from utils.item_utils import *
from utils.open_ai_utils import *
from datetime import datetime
import json
from utils.twilio_utils import send_expiration_reminder, send_high_temperature_warning


app = Flask(__name__)

pub_key_name = 'app/utils/keys/server_public_key_fresh.pem'
private_key_name = 'app/utils/keys/server_private_key_fresh.pem'




# This is a wrapper that checks if the API key is present in the header
def require_api_key_with_time(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-KEY'): # Check if the header is present
            if request.headers.get('DEVICE') == 'CAMERA':
                
                api_key_time = decode_decrypt_api_key(
                                            encoded_api_key=request.headers['X-API-KEY'],
                                            private_key_name=private_key_name
                                            )
                
                api_key_time = api_key_time.decode('utf-8').split(',')
                api_key = api_key_time[0]
                time_stamp = api_key_time[1]
                

                account_id = get_account_id_from_api_key(api_key=api_key,time_stamp=time_stamp)
                
                return f(account_id=account_id, *args, **kwargs)
            elif request.headers.get('DEVICE') == 'MOBILE':
                account_id = get_account_id_from_api_key(api_key=request.headers['X-API-KEY'],time_stamp=str(datetime.now().timestamp()))
                return f(account_id=account_id, *args, **kwargs)
            else:
                return jsonify({"error": "API key validation failed"}), 403
    return decorated_function









@app.route('/')
def index():
    return 'Hello, World!'



@app.route('/item/upload', methods=['POST'])
@require_api_key_with_time
def upload_image(account_id: str):
    bucket_name = 'fridgepictures'
    if 'image' in request.files:
        image = request.files['image']
        timestamp = request.form.get('timestamp',None)  # Get timestamp from form data
        classname = request.form.get('classname',None)  # Get classname from form data
        if not timestamp or not classname:
            return jsonify({"error":'Timestamp and classname are required'}), 400

        return add_item_to_s3_dynamoDB(image, account_id, classname, timestamp)
    return jsonify({'error': 'No image found in request'}), 400



@app.route('/item/photo/<item_id>', methods=['GET'])
@require_api_key_with_time
def get_item_photo(item_id: str,account_id: str):
    photo_url = get_item_photo_from_s3(account_id=account_id, item_id=item_id)
    print(photo_url)
    if photo_url:
        # Properly return the JSON response with a 200 status code
        return jsonify({'real_photo_path': photo_url}), 200
    else:
        # Return a JSON error message with a 404 status code
        return jsonify({'error': 'Item not found'}), 404

@app.route('/item/update', methods=['POST'])
@require_api_key_with_time
def update_item(account_id: str):
    data = json.loads(request.data.decode('utf-8'))
  
    result = update_item_in_fridge(data=data)
    if result:
        return jsonify({'message': 'Item updated successfully'}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404


@app.route('/item/<item_id>', methods=['DELETE'])
@require_api_key_with_time
def delete_item(item_id: str, account_id: str):

    

    response = delete_item_from_s3_dynamoDB(account_id, item_id)
    if response:
        return jsonify({'message': 'Item deleted successfully'}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404
    
    



#Endpoint to post and get the most recent photo of the fridge
@app.route('/fridge/photo', methods=['POST', 'GET'])
@require_api_key_with_time
def fridge_photo(account_id: str):
    bucket_name = 'fridgepictures'
    object_name = f'{account_id}'  # Assuming the image is saved as '<account_id>.jpg'

    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
           

            save_path = f'uploads/{account_id}.jpeg' 
            image.save(save_path)
    
            bucket = get_s3_bucket(bucket_name)
            data = open(f'uploads/{account_id}.jpeg', 'rb')

            bucket.put_object(Key=object_name, Body=data)
            return jsonify({'message': 'Image uploaded successfully'}), 200
            
    else:
        url = get_presigned_url(bucket_name, object_name)
        if url:
            return jsonify({'url': url}), 200
        else:
            return jsonify({'error': 'Unable to generate URL'}), 500

             

# Upload current temperature and humidity of the fridge

@app.route('/fridge/conditions', methods=['POST','GET'])
@require_api_key_with_time
def upload_fridge_conditions(account_id: str):
    
    if request.method == 'GET':
        conditions = get_latest_fridge_conditions_from_dynamoDB('fridge_conditions', account_id)
       
        return jsonify(conditions), 200
    else:
    
        data = json.loads(request.data.decode('utf-8'))
        
       
        temperature = Decimal(data.get('temperature'))
        humidity = Decimal(data.get('humidity'))
        if temperature > 76:
            send_high_temperature_warning(temperature=temperature)
        timestamp = data.get('timestamp')
        dynamo_response = store_temperature_and_humidity_in_dynamoDB('fridge_conditions', {'account_id': account_id, 'temperature': temperature, 'humidity': humidity, 'timestamp': timestamp})
        
        return jsonify({'message': 'Fridge conditions uploaded successfully'}), 200



@app.route('/fridge/conditions/historical', methods=['GET'])
@require_api_key_with_time
def get_historical_fridge_conditions(account_id: str):
    conditions = get_historical_fridge_conditions_from_dynamoDB('fridge_conditions', account_id)
    return jsonify(conditions), 200




@app.route('/fridge/items', methods=['GET'])
@require_api_key_with_time
def get_fridge_items(account_id):
    try:
        items = list_items_in_fridge(account_id)
        for item in items:
            signed_url = get_presigned_url('fridgepictures', item['real_photo_path'], expiration=100)
            item['s3_url'] = signed_url
        
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




# This is a public endpoint that sends the public key to the client
@app.route('/public_key', methods=['GET'])
def public_key():

    return load_public_key(pub_key_name=pub_key_name), 200


# This is a test endpoint that recieves the encrypted api key from the client in the header and decrypts it
@app.route('/encrypted_api_key_header', methods=['GET'])
@require_api_key_with_time
def encrypted_api_key_header(account_id: str):
    print("Account ID retreived from the API Key: ", account_id)
    

    return jsonify({'message': f'API key wrapper validation successful: account_id {account_id}'}), 200

    



# This endpoint returns the html file called index.html in the templates folder
#This file takes a presigned URL and displays the image at that URL, and gets the current photo and temperature and humidity of the fridge
@app.route('/fridge_web', methods=['GET'])
def fridge_web():

    conditions = get_latest_fridge_conditions_from_dynamoDB('fridge_conditions', 'XXXXXX')

    temp = str(conditions[0]['temperature'])
    humid = str(conditions[0]['humidity'])
  
    url = get_presigned_url('fridgepictures', 'XXXXXX',expiration=100)
    
    return render_template('index.html', photo_url=url, temperature=temp, humidity=humid)



@app.route('/mobile/recipe', methods=['GET'])
@require_api_key_with_time
def recipe_suggestion(account_id: str):
    items = list_items_in_fridge(account_id)
    items = [item['classname'] for item in items]
    
    recipe = get_recipe(items)
    return jsonify({'recipe': recipe}), 200



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# python basic_webapp.py
# to run the webapp, run the following command in the terminal