import sqlite3 
import functools

def with_db_connection(func):
    """Decorator that automatically handles database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Connect to database
        conn = sqlite3.connect('users.db')
        try:
            # Pass connection as first argument to the function
            result = func(conn, *args, **kwargs)
            return result
        except Exception as e:
            # Re-raise the exception
            raise e
        finally:
            # Always close the connection
            conn.close()
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone()

# Setup test database
def setup_test_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'John Doe', 'john@example.com')")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_test_database()
    # Fetch user by ID with automatic connection handling 
    user = get_user_by_id(user_id=1)
    print(user)
