
from twilio.rest import Client
from datetime import datetime, timedelta


twilio_number = '+XXXXXXXXXXXXX'
jack_number = '+XXXXXXXXXXXXX'


account_sid = 'twillio_account_ID'
auth_token = 'XXXXXXXXXX'
#client = Client(account_sid, auth_token)

#message = client.messages.create(
#  from_=twilio_number,
#  body='Hello from Twilio',
#  to=jack_number
#)

#print(message.sid)



def send_expiration_reminder(phone_number:str, item_list: list):

    


    new_text = ""
    for item in item_list:
        # Parse the datetime string into a datetime object
        datetime_obj = datetime.strptime(item['expiration_date'], "%Y-%m-%d")

        # Convert the datetime object to the desired format
        formatted_date = datetime_obj.strftime("%B %d, %Y")
        new_text += f"{item['classname']} expires on {formatted_date}\n"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=twilio_number,
        body=new_text,
        to=jack_number
    )

    
    return True


def send_high_temperature_warning(temperature: float):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=twilio_number,
        body=f"Your fridge temperature is above set threshold. Current Temp: {temperature}°F",
        to=jack_number
    )

    return True