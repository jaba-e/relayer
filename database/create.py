from connect import connectDB
import mysql.connector

TABLES = {}
TABLES['api1_response'] = (
    "CREATE TABLE `api1_response` ("
    "  `msg_id` int UNIQUE NOT NULL,"
    "  `message` varchar(5000) NOT NULL,"
    "  `sender` varchar(200) NOT NULL,"
    "  `created_at` datetime NOT NULL DEFAULT NOW(),"
    "  PRIMARY KEY (`msg_id`)"
    ") ENGINE=InnoDB")

TABLES['api2_response'] = (
    "CREATE TABLE `api2_response` ("
    "  `msg_id` int UNIQUE NOT NULL,"
    "  `choices_text` varchar(5000) NOT NULL,"
    "  `api_response` json DEFAULT NULL,"
    "  `created_at` datetime NOT NULL DEFAULT NOW(),"
    "  PRIMARY KEY (`msg_id`)"
    ") ENGINE=InnoDB")


def createTable():
    mydb = connectDB()
    mycursor = mydb.cursor()

    try:
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                mycursor.execute(table_description)
            except mysql.connector.Error as err:
                print("Failed creating database, please check sql syntax.", err)
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

createTable()