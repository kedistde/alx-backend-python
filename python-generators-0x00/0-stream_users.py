#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

HOST = "localhost"
USER = "root"
PASSWORD = ""
DB_NAME = "ALX_prodev"
TABLE = "user_data"

def stream_users():
    """
    Generator that yields one row at a time from user_data.
    """

    try:
        conn = mysql.connector.connect(
            host=HOST, user=USER, password=PASSWORD, database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT user_id, name, email, age FROM {TABLE}")
        
        for row in cursor:
            yield row

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Example usage:
if __name__ == "__main__":
    for user in stream_users():
        print(user)
