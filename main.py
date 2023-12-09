import os
import json
import requests
from database.connect import connect_db 
from dotenv import load_dotenv
import sqlalchemy

load_dotenv()
PENDING_PROMPT_LENGTH = 1
SUCCESS_RESPONSE = "Response has been created"

def answer_prompts():
    try:
        prompts = requests.get(url = os.getenv('CUSTOM_CHATBOT_API')).json()
        pending_prompts = [p for p in prompts if len(p["message_response"]) <= PENDING_PROMPT_LENGTH]
        answers = []

        for pending_prompt in pending_prompts:
            chatgpt_answer = ask_chatgpt(pending_prompt['message'])
            if not chatgpt_answer:
                return(500)
            
            if not insert_data(pending_prompt, chatgpt_answer):
                return(500)

            answer = {
                "msg_id": pending_prompt["msg_id"],
                "message": pending_prompt["message"],
                "sender": pending_prompt["sender"],
                "message_response": chatgpt_answer 
            }
            answers.append(answer)

        response_code=send_answers(answers)
        return(response_code)

    except Exception as e:
        print("Exception occurred", e)
        return(500)

def ask_chatgpt(prompt):
    try:
        chatgpt_input = {
            "model" : "text-davinci-002",
            "prompt": prompt,
            "max_tokens": os.getenv('MAX_TOKENS'),
            "temperature": os.getenv('TEMPERATURE'),
        }

        chatgpt_response = requests.post(
            url = os.getenv('OPENAI_API'),
            headers=get_header('OPENAI'),
            data = json.dumps(chatgpt_input)).json()
        
        return chatgpt_response["choices"][0]["text"].replace("\n", "") # Since chatgpt makes multiple suggestions, only taking first one.
    
    except Exception as e:
        print("Error occurred:", e)

def insert_data(pending_prompt, chatgpt_answer):
    try:
        db = connect_db()
        db.execute(sqlalchemy.text(
            'insert into custom_chatbot_response (msg_id, message, sender) values ("{}", "{}", "{}")'
            .format(pending_prompt['msg_id'], pending_prompt['message'], pending_prompt['sender'])))
        
        db.execute(sqlalchemy.text(
            'insert into chatgpt_response (msg_id, choices_text) values ("{}", "{}")'
            .format(pending_prompt['msg_id'], chatgpt_answer)))

        db.close()
        return 200
    except Exception as e:
        print("Error occurred:", e)
        db.rollback()
    finally:
        db.close()

def send_answers(answers):
    try:
        if not answers:
            return 200
        
        custom_chatbot_response = requests.post(
            url = os.getenv('CUSTOM_CHATBOT_API'),
            headers=get_header(),
            data = json.dumps(answers)).json()

        return 200 if custom_chatbot_response == SUCCESS_RESPONSE else 500
    except Exception as e:
        print("Error occurred:", e)
        return 500

def get_header(api=None):
    headers = {"Content-Type": "application/json"}
    if api == "OPENAI":
        headers['Authorization'] = f"Bearer {os.getenv('OPENAI_TOKEN')}"
    return headers

if __name__ == "__main__":
    answer_prompts()