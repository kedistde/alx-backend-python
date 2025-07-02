#!/usr/bin/env python3
import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = ""
DB = "ALX_prodev"
TABLE = "user_data"

def stream_users_in_batches(batch_size):
    """
    Generator yielding batches of rows (as dicts) from the user_data table.
    """
    conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DB)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT user_id, name, email, age FROM {TABLE}")
    # Single loop for batching via fetchmany()
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch
    cursor.close()
    conn.close()

def batch_processing(batch_size):
    """
    Generator yielding user dicts over age > 25, processing in batches.
    """
    # Loop 1: iterate batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 2: filter within each batch
        for user in batch:
            if user['age'] > 25:
                yield user

# Example usage:
if __name__ == "__main__":
    for u in batch_processing(batch_size=50):
        print(u)
