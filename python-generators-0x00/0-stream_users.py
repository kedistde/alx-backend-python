#!/usr/bin/python3
def stream_users():
    from itertools import islice
    stream_users = __import__('0-stream_users')


    for user in islice(stream_users(), 6):
        print(user)
