import os
import json
import requests
from database.connect import connectDB 
from dotenv import load_dotenv
import sqlalchemy

load_dotenv()

MESSAGES_API = os.getenv('MESSAGES_API')
TEXT_COMPLETION_API = os.getenv('TEXT_COMPLETION_API')
API2_TOKEN = os.getenv('API2_TOKEN')

def send_new_message_response(request):
    api1_headers = {
        "Content-Type": "application/json",
    }

    api2_headers = {
        "Content-Type": "application/json",
        'Authorization': f"Bearer {API2_TOKEN}"
    }

    try:
        mydb = connectDB()
        
        api1_response = requests.get(url = MESSAGES_API).json()
        new_messages = [p for p in api1_response if len(p["message_response"])  <= 1]
        completed_new_message = []
        for new_message in api1_response:

            api1_insert_script = sqlalchemy.text('insert into api1_response (msg_id, message, sender) values ("{}", "{}", "{}")'.format(new_message['msg_id'], new_message['message'], new_message['sender']))
            mydb.execute(api1_insert_script)

            api2_data = {
                "model" : "text-davinci-002",
                "prompt": new_message["message"],
                "max_tokens": 2000,
                "temperature": 0, # Later set to 100.
            }

            text_completion_response = requests.post(
                url = TEXT_COMPLETION_API, 
                data = json.dumps(api2_data), 
                headers=api2_headers).json()

            clean_choices_text = text_completion_response["choices"][0]["text"].replace("\n", "") # Getting only first element. Later we can add more.

            new_message_data = {
                "msg_id": new_message["msg_id"],
                "message": new_message["message"],
                "sender": new_message["sender"],
                "message_response": clean_choices_text 
            }

            completed_new_message.append(new_message_data)
            api2_insert_script = sqlalchemy.text('insert into api2_response (msg_id, choices_text) values ("{}", "{}")'.format(new_message['msg_id'], clean_choices_text))

            mydb.execute(api2_insert_script)

        if completed_new_message:
            message_post_response = requests.post(
                url = MESSAGES_API, 
                data = json.dumps(completed_new_message), 
                headers=api1_headers).json()

            if message_post_response == "Response has been created":
                return(200)
            else:
                return(500)

        mydb.close()
        return(200)

    except Exception as e:
        print("Exception occured", e)
        return(500)


send_new_message_response("s")