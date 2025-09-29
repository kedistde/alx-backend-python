import sqlite3
import functools

def log_queries(func):
    """Decorator that logs SQL queries before executing them."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from kwargs or args
        query = kwargs.get('query', None)
        if not query and args:
            query = args[0] if isinstance(args[0], str) else None
        
        print(f"Executing SQL Query: {query}")
        
        # Execute the original function
        result = func(*args, **kwargs)
        
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Create test database and table
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
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('John Doe', 'john@example.com')")
    cursor.execute("INSERT OR IGN
