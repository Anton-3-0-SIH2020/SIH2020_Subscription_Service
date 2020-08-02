import psycopg2
from configparser import ConfigParser

configure = ConfigParser()
configure.read("secret.ini")

DATABASE = configure.get("POSTGRES", "DATABASE")
USER = configure.get("POSTGRES", "USER")
PASSWORD = configure.get("POSTGRES", "PASSWORD")
HOST = configure.get("POSTGRES", "HOST")
PORT = configure.get("POSTGRES", "PORT")

# Date format 01-Aug-2020


def get_user_list():
    users = []
    connection = psycopg2.connect(
        user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE,
    )
    cursor = connection.cursor()
    query = f"SELECT * FROM subscriber_list"
    cursor.execute(query)
    for data in cursor:
        user = {
            "uid": data[0],
            "email": data[1],
        }
        users.append(user)
    cursor.close()
    connection.close()
    return users