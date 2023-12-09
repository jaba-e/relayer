## Introduction
This is a script for answering chatbot prompts using chatgpt text-davinci-002 model.

## Local setup

1. Create virtual environment: `python3 -m venv env`
2. Activate virtual environment: `source env/bin/activate`
3. Install packages: `pip3 install -r requirements.txt`
4. Create a `.env` file. `cp .env.example .env` and update the necessary variables.
5. Create a mysql DB. `docker compose up -d`
6. Create tables: `python3 database/create.py`
7. Run the script: `python3 main.py`

## How infrastructure works

We use Google Cloud Platform.

1. Script is deployed on CLOUD FUNCTION.
2. CLOUD SCHEDULER triggers the CLOUD FUNCTION every minute.
3. Script saves CUSTOM_CHATBOT_API, OPENAI_API data to CLOUD SQL and send prompts answer to CUSTOM_CHATBOT_API.