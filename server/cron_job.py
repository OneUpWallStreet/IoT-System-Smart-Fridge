from datetime import datetime 
from utils.dynamo_utils import list_items_in_fridge, list_items_expiring_soon, update_item_in_fridge
from utils.twilio_utils import send_expiration_reminder
import json
                         
#with open('/home/ubuntu/fridge_cam/server/cron_log.log', 'w') as f:
#    f.write(f'The cron job is working: {datetime.now()}')
    
print(f'The cron job is working: {datetime.now()}')

# Need to scan all items in the fridge_items table and check the expiration date
# If the expiration date is today, then send a notification to the user

# Get all items in the fridge where the expiration date is today

# Make list of account_id to item


# Mark all expired items as expired

expired_items = list_items_expiring_soon(account_id='XXXXXXX',days=0,table_name='fridge_items')
for item in expired_items:
    item['expired'] = True
    response = update_item_in_fridge(data=item)
print(json.dumps(expired_items, indent=4))





#SEND NOTIFICATION TO USER

jack_number = '+XXXXXXXXXXXXX'
swarom_number = '+XXXXXXXXXXXXX'


items_expiring = list_items_expiring_soon(account_id='XXXXXX',days=5,table_name='fridge_items')


send_expiration_reminder(phone_number=jack_number,item_list=items_expiring)
