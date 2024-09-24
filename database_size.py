import mysql.connector

# Database connection parameters
db_config = {
    'user': 'root',
    'password': 'WYzMP2trak',
    'host': 'localhost',
    'database': 'information_schema'
}

def calculate_database_size():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
        SELECT table_schema AS "botransactions", 
        ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size in (MB)" 
        FROM information_schema.TABLES
        WHERE table_schema = "botransactions" 
        GROUP BY table_schema;
        """

        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            print(f"Database: {result[0]}, Size: {result[1]} MB")
        else:
            print("Database not found or no tables present.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    calculate_database_size()
