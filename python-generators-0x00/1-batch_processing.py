#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')
def stream_users_in_batches(batch_size):
    try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: process each user in batch
        for user in batch:
            if user['age'] > 50: 
                yield user
##### print processed users in a batch of 50

    
