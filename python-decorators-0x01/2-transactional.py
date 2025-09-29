import sqlite3 
import functools

# Copy the with_db_connection decorator from previous task
def with_db_connection(func):
    """Decorator that automatically handles database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        except Exception as e:
            raise e
        finally:
            conn.close()
    return wrapper

def transactional(func):
    """Decorator that manages database transactions."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Execute the function
            result = func(conn, *args, **kwargs)
            # If no exception, commit the transaction
            conn.commit()
            return result
        except Exception as e:
            # If exception occurs, rollback the transaction
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise e
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"Updated user {user_id} email to {new_email}")

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
    # Update user's email with automatic transaction handling 
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    
    # Verify the update
    @with_db_connection
    def get_user(conn, user_id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()
    
    user = get_user(user_id=1)
    print(f"Updated user: {user}")
