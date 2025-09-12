import sqlite3
import os

class DatabaseConnection:
    """A context manager for handling database connections automatically."""
    
    def __init__(self, database_path=":memory:"):
        """
        Initialize the DatabaseConnection context manager.
        
        Args:
            database_path (str): Path to the SQLite database file. 
                               Defaults to in-memory database.
        """
        self.database_path = database_path
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """Enter the context - establish database connection."""
        try:
            self.connection = sqlite3.connect(self.database_path)
            self.cursor = self.connection.cursor()
            print(f"Connected to database: {self.database_path}")
            return self.cursor
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context - close database connection."""
        if self.cursor:
            self.cursor.close()
            print("Cursor closed")
        
        if self.connection:
            if exc_type is None:  # No exception occurred
                self.connection.commit()
                print("Changes committed to database")
            else:
                self.connection.rollback()
                print("Changes rolled back due to exception")
            
            self.connection.close()
            print("Database connection closed")
        
        # Return False to propagate exceptions, True to suppress them
        return False


# Example usage with the context manager
def main():
    # Create a sample database with some test data
    sample_db = "test_users.db"
    
    # First, create the database and table with sample data
    with sqlite3.connect(sample_db) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        cursor.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            [
                ("Alice Johnson", "alice@example.com"),
                ("Bob Smith", "bob@example.com"),
                ("Charlie Brown", "charlie@example.com")
            ]
        )
        conn.commit()
    
    # Use our custom context manager to query the database
    print("\nUsing DatabaseConnection context manager:")
    print("-" * 50)
    
    try:
        with DatabaseConnection(sample_db) as cursor:
            # Execute the query
            cursor.execute("SELECT * FROM users")
            
            # Fetch and print the results
            results = cursor.fetchall()
            print("\nQuery Results:")
            print("ID | Name           | Email")
            print("-" * 40)
            
            for row in results:
                print(f"{row[0]:2} | {row[1]:14} | {row[2]}")
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    
    finally:
        # Clean up the sample database file
        if os.path.exists(sample_db):
            os.remove(sample_db)
            print(f"\nCleaned up: Removed {sample_db}")


if __name__ == "__main__":
    main()
