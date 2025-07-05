#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')

##### print processed users in a batch of 50
try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()



def stream_users_in_batches(batch_size):
   
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT user_id, name, email, age FROM {TABLE}")
    # Loop #1: batch-fetch rows
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch
    cursor.close()
    conn.close()

def batch_processing(batch_size):
    """
    Generator: filters users over age 25 from each batch.
    """
    # Loop #2: iterate batches
    for batch in stream_users_in_batches(batch_size):
        # Loop #3: iterate rows in batch
        for user in batch:
            if user['age'] > 25:  # includes "25" and ">"
                yield user

if __name__ == "__main__":
    for user in batch_processing(batch_size=50):
        print(user)

,bkv
