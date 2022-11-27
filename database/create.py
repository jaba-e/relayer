from connect import connectDB
import sqlalchemy

TABLES = {}
TABLES['api1_response'] = (
    "CREATE TABLE `api1_response` ("
    "  `msg_id` int UNIQUE NOT NULL,"
    "  `message` TEXT NOT NULL,"
    "  `sender` varchar(200) NOT NULL,"
    "  `created_at` datetime NOT NULL DEFAULT NOW(),"
    "  PRIMARY KEY (`msg_id`)"
    ") ENGINE=InnoDB")

TABLES['api2_response'] = (
    "CREATE TABLE `api2_response` ("
    "  `msg_id` int UNIQUE NOT NULL,"
    "  `choices_text` TEXT NOT NULL,"
    # "  `api_response` TEXT DEFAULT NULL,"
    "  `created_at` datetime NOT NULL DEFAULT NOW(),"
    "  PRIMARY KEY (`msg_id`)"
    ") ENGINE=InnoDB")


def createTable():
    mydb = connectDB()

    try:
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                mydb.execute(table_description)
            except Exception as err:
                print("Failed creating database, please check sql syntax.", err)
    except Exception as err:
        print("Failed creating database: {}".format(err))
        exit(1)

createTable()