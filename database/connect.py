import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def connectDB():
    try: 
        mydb = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            port = os.getenv('DB_PORT'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )

        return mydb
        
    except mysql.connector.Error as err:
        print("Failed connecting database: {}".format(err))