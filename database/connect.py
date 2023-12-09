import os
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    try: 
        db = sqlalchemy.create_engine(
          sqlalchemy.engine.url.URL(
            drivername='mysql+pymysql',
            host = os.getenv('DB_HOST'),
            port = os.getenv('DB_PORT'),
            username=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
          ),
          pool_size=5,
          max_overflow=2,
          pool_timeout=30,
          pool_recycle=1800
        )

        return db.connect()
        
    except Exception as err:
        print("Failed connecting database: {}".format(err))

connect_db()
