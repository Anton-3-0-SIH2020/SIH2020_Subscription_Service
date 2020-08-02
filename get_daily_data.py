import datetime
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


def get_daily_data():
    ca_array = []
    now = datetime.datetime.now().strftime("%d-%b-%Y")
    connection = psycopg2.connect(
        user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE,
    )
    cursor = connection.cursor()
    query = f"SELECT * FROM latest_nse_ca WHERE ex_date = date('{now}')"
    cursor.execute(query)
    for data in cursor:
        corporate_action = {
            "symbol": data[1],
            "purpose": data[5],
            "ex_date": data[6].strftime("%d-%b-%Y"),
            "record_date": data[7],
            "bc_start_date": data[8],
            "bc_end_date": data[9],
        }
        ca_array.append(corporate_action)
    query = f"SELECT * FROM latest_mc_ca WHERE ex_date = date('{now}')"
    cursor.execute(query)
    for data in cursor:
        corporate_action = {
            'company_name': data[1],
            'purpose': data[2],
            'ex-date': data[5].strftime("%d-%b-%Y"),
            'record_date': data[4],
            'bc_start_date': 'None',
            'bc_end_date': 'None',
        }
        ca_array.append(corporate_action)
    query = f"SELECT * FROM latest_bse_ca WHERE ex_date = date('{now}')"
    cursor.execute(query)
    for data in cursor:
        corporate_action = {
            'security_code': data[1],
            'purpose': data[4],
            'ex_date': data[3].strftime("%d-%b-%Y"),
            'record_date': data[5],
            'bc_start_date': data[6],
            'bc_end_date': data[7],
        }
        ca_array.append(corporate_action)
    cursor.close()
    connection.close()
    return ca_array