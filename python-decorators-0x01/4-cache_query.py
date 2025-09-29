import time
import sqlite3 
import functools
import hashlib

# Global cache dictionary
query_cache = {}

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

def cache_query(func):
    """Decorator that caches query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Create a cache key from the query
        cache_key = hashlib.md5(query.encode()).hexdigest()
        
        # Check if result is in cache
        if cache_key in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[cache_key]
        
        # If not in cache, execute the query and cache the result
        print(f"Executing query and caching result: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[cache_key] = result
        
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

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
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('John Doe', 'john@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES ('Jane Smith', 'jane@example.com')")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_test_database()
    
    # First call will cache the result
    print("First call:")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Results: {users}")
    
    print("\n" + "="*50 + "\n")
    
    # Second call will use the cached result
    print("Second call:")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Results: {users_again}")
    
    print("\n" + "="*50 + "\n")
    
    # Different query will not use cache
    print("Different query:")
    specific_user = fetch_users_with_cache(query="SELECT * FROM users WHERE id = 1")
    print(f"Results: {specific_user}")
