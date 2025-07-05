#!/usr/bin/python3

seed = __import__('seed')

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print(f"connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()


def connect_to_prodev():
    return mysql.connector.connect(
        host=HOST, user=USER, password=PASSWORD, database=DB_NAME
    )

def create_table(conn):
    cursor = conn.cursor()
    create_stmt = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,2) NOT NULL,
        INDEX (user_id)
    ) ENGINE=InnoDB
    """
    cursor.execute(create_stmt)
    conn.commit()
    cursor.close()

def insert_data(conn, data_rows):
    cursor = conn.cursor()
    for row in data_rows:
        # Check existence
        cursor.execute(
            f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE email = %s",
            (row["email"],)
        )
        (count,) = cursor.fetchone()
        if count == 0:
            user_id = str(uuid.uuid4())
            cursor.execute(
                f"INSERT INTO {TABLE_NAME} (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (user_id, row["name"], row["email"], row["age"])
            )
    conn.commit()
    cursor.close()

def load_csv(filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def main():
    # Step 1: connect to MySQL server (no database)
    conn = connect_db()
    create_database(conn)
    conn.close()

    # Step 2: connect to ALX_prodev
    conn = connect_to_prodev()
    create_table(conn)

    # Step 3: load sample data
    data = load_csv(CSV_FILE)

    # Step 4: insert if not exists
    insert_data(conn, data)

    conn.close()
    print("✅ Database seeded successfully.")

if __name__ == "__main__":
    main()
