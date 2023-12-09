from connect import connect_db

TABLES = {}
TABLES['custom_chatbot_response'] = (
    "CREATE TABLE `custom_chatbot_response` ("
    "  `msg_id` int UNIQUE NOT NULL,"
    "  `message` TEXT NOT NULL,"
    "  `sender` varchar(200) NOT NULL,"
    "  `created_at` datetime NOT NULL DEFAULT NOW(),"
    "  PRIMARY KEY (`msg_id`)"
    ") ENGINE=InnoDB")

TABLES['chatgpt_response'] = (
    "CREATE TABLE `chatgpt_response` ("
    "  `msg_id` int UNIQUE NOT NULL,"
    "  `choices_text` TEXT NOT NULL,"
    "  `created_at` datetime NOT NULL DEFAULT NOW(),"
    "  PRIMARY KEY (`msg_id`)"
    ") ENGINE=InnoDB")


def create_table():
    mydb = connect_db()

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

if __name__ == "__main__":
    create_table()