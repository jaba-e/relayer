import os
import json
import requests
from pathlib import Path
from database.connect import connectDB 
from dotenv import load_dotenv

load_dotenv()

MESSAGES_API = os.getenv('MESSAGES_API')
TEXT_COMPLETION_API = os.getenv('TEXT_COMPLETION_API')
API2_TOKEN = os.getenv('API2_TOKEN')

def send_new_message_response():
    api1_headers = {
        "Content-Type": "application/json",
    }

    api2_headers = {
        "Content-Type": "application/json",
        'Authorization': f"Bearer {API2_TOKEN}"
    }

    try:
        mydb = connectDB()
        mycursor = mydb.cursor()
        response_data = []
        api1_response = requests.get(url = MESSAGES_API).json()
        new_messages = [p for p in api1_response if "message_response" not in p]
        # new_messages = [p for p in api1_response if "message_response" in p]

        for new_message in new_messages:

            insert_script = "INSERT INTO api1_response (msg_id, message, sender) VALUES (%s, %s, %s)"

            val = (
                new_message["msg_id"], 
                new_message["message"], 
                new_message["sender"]
            )

            mycursor.execute(insert_script, val)
            mydb.commit()
            print(mycursor.rowcount, "api1_response was inserted.")

            api2_data = {
                "model" : "text-davinci-002",
                "prompt": new_message["message"],
                "max_tokens": 2000,
                "temperature": 0,
            }

            text_completion_response = requests.post(
                url = TEXT_COMPLETION_API, 
                data = json.dumps(api2_data), 
                headers=api2_headers).json()


            clean_choices_text = text_completion_response["choices"][0]["text"].replace("\n", "")

            api1_return_data = {
                "msg_id": new_message["msg_id"],
                "message": new_message["message"],
                "sender": new_message["sender"],
                "message_response": clean_choices_text # Getting only first element. Later we can add more.
            }

            response_data.append(api1_return_data)

            insert_script = "INSERT INTO api2_response (msg_id, choices_text, api_response) VALUES (%s, %s, %s)"
            val = (
                new_message["msg_id"], 
                clean_choices_text, 
                json.dumps(text_completion_response)
            )
            mycursor.execute(insert_script, val)
            mydb.commit()

        if len(response_data) > 0:
            message_post_response = requests.post(
                url = MESSAGES_API, 
                data = json.dumps(response_data), 
                headers=api1_headers).json()

        mydb.disconnect()

    except Exception as e:
        print("e", e)


send_new_message_response()