import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="achu",
        database="Vehicle_Service_Management"
    )
