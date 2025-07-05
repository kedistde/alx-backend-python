#!/usr/bin/env python3
import mysql.connector

def stream_user_ages():
  
    conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DB)
    cursor = conn.cursor()
    cursor.execute(f"SELECT age FROM {TABLE}")
    
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

    avg = total / count if count else 0
    print(f"Average age of users: {avg}")

if __name__ == "__main__":
    compute_average_age()
