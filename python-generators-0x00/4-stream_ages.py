#!/usr/bin/env python3
seed = __import__('seed')


def stream_user_ages():
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT age FROM user_data")
    # Loop #1: fetch rows lazily using cursor iteration
    for (age,) in cursor:
        yield age
    cursor.close()
    conn.close()

def compute_average_age():
    
    total = 0.0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    average = total / count if count else 0
    print(f"Average age of users: {average}")

if __name__ == "__main__":
    compute_average_age()

   
