# Chatbot Prompt Answering Script using GPT-3 (chatgpt text-davinci-002 model)

## Introduction

This script utilizes the chatgpt text-davinci-002 model by OpenAI to generate responses for various chatbot prompts.

## Local Setup

To set up the script locally for testing or development purposes, follow these steps:

1. **Create a Virtual Environment:**
    ```bash
    python3 -m venv env
    ```

2. **Activate the Virtual Environment:**
    ```bash
    source env/bin/activate
    ```

3. **Install Required Packages:**
    ```bash
    pip3 install -r requirements.txt
    ```

4. **Configure Environment Variables:**
    - Create a `.env` file: 
      ```bash
      cp .env.example .env
      ```
    - Update the necessary variables in the `.env` file.

5. **Set Up MySQL Database:**
    - Start a MySQL container using Docker:
      ```bash
      docker compose up -d
      ```
    - Create tables within the database:
      ```bash
      python3 database/create.py
      ```

6. **Run the Script:**
    ```bash
    python3 main.py
    ```

## How should you deploy it

1. **Deployment on Cloud Function:**
   - Use AWS Lambda or GCP cloud function.

2. **Response Handling:**
   - Upon triggering, the script generates responses to prompts and sends them to CUSTOM_CHATBOT_API.
