## Installation

1. Create virtual environment: `python3 -m venv env`
2. Activate virtual environment: `source env/bin/activate`
3. Install packages: `pip3 install -r requirements.txt`
4. Start a MySql database with docker using: `docker-compose up -d`.
5. Create a `.env` file and add the `DATABASE_URL` environment variable.
    - The `.env.example` file is provided as reference.

5. Start the project: `python3 main.py`

## Infra explanation.

1. Script is deployed on CLOUD FUNCTION.
2. CLOUD SCHEDULER triggers CLOUD FUNCTION every minute.
3. Script save API1, API2 data to CLOUD SQL and returns completed data.