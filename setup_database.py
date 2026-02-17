import mysql.connector
from mysql.connector import Error

def setup_database():
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Y@sh8105",
            database="Transplant"
        )
        cursor = conn.cursor()

        # Create organs table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS organs (
                name VARCHAR(50) PRIMARY KEY,
                description TEXT
            )
        """)

        # List of organs to ensure they exist
        organs = [
            ("Kidney", "Vital organ that filters blood"),
            ("Heart", "Vital organ that pumps blood"),
            ("Liver", "Vital organ that processes nutrients"),
            ("Lung", "Vital organ for breathing"),
            ("Pancreas", "Organ that produces insulin"),
            ("Cornea", "Transparent part of the eye")
        ]

        # Insert organs if they don't exist
        for organ in organs:
            cursor.execute("""
                INSERT IGNORE INTO organs (name, description)
                VALUES (%s, %s)
            """, organ)

        # Drop existing donors table if it exists
        cursor.execute("DROP TABLE IF EXISTS donors")

        # Create donors table without foreign key constraint
        cursor.execute("""
            CREATE TABLE donors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(10) NOT NULL,
                contact_number VARCHAR(15) NOT NULL,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL,
                aadhaar VARCHAR(20),
                address TEXT,
                blood_type VARCHAR(5) NOT NULL,
                organ VARCHAR(50) NOT NULL,
                medical_history TEXT,
                status VARCHAR(20) DEFAULT 'pending'
            )
        """)

        # Commit the changes
        conn.commit()
        print("Database setup completed successfully!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database() 