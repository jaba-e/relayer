## Introduction
This is a script for answering chatbot prompts using chatgpt text-davinci-002 model.

## Local setup

1. Create virtual environment: `python3 -m venv env`
2. Activate virtual environment: `source env/bin/activate`
3. Install packages: `pip3 install -r requirements.txt`
4. Start a MySql database with docker using: `docker-compose up -d`.
5. Create a `.env` file and add the `DATABASE_URL` environment variable.
    - The `.env.example` file is provided as reference.

5. Start the project: `python3 main.py`

## How infrastructure works

We use Google Cloud Platform.

1. Script is deployed on CLOUD FUNCTION.
2. CLOUD SCHEDULER triggers the CLOUD FUNCTION every minute.
3. Script saves CUSTOM_CHATBOT_API, OPENAI_API data to CLOUD SQL and send prompts answer to CUSTOM_CHATBOT_API.