def paginate_users(page_size, offset):
    """
    Fetches a single batch (page) of rows using SQL LIMIT/OFFSET.
    Returns a list of row dicts.
    """
    conn = mysql.connector.connect(
        host=HOST, user=USER, password=PASSWORD, database=DB
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        f"SELECT user_id, name, email, age FROM {TABLE} "
        f"ORDER BY user_id LIMIT %s OFFSET %s",
        (page_size, offset)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
def batch_processing(batch_size):
    """
    Generator: processes batches from stream, yielding users over age > 25.
    """
    # Loop 2: iterate through batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: process each user in batch
        for user in batch:
            if user['age'] > 25:  # filter for age over 25
                yield user
def lazy_paginate(page_size):
    """
    Generator that lazily fetches pages and yields rows one at a time.
    Only one loop is used here.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        for row in page:
            yield row
        offset += page_size
