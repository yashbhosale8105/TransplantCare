import mysql.connector
from mysql.connector import Error

def setup_database():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Y@sh8105"
        )
        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute("DROP DATABASE IF EXISTS sbl")
        cursor.execute("CREATE DATABASE sbl")
        cursor.execute("USE sbl")

        # Create users table
        cursor.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        # Create game_sessions table
        cursor.execute("""
            CREATE TABLE game_sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                score INT NOT NULL,
                level_reached INT NOT NULL,
                session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Create high_scores table
        cursor.execute("""
            CREATE TABLE high_scores (
                user_id INT NOT NULL,
                high_score INT NOT NULL,
                games_played INT DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        conn.commit()
        print("Database and tables created successfully!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database() 