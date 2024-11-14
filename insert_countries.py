
import sys
import mysql.connector
from mysql.connector import errorcode
import csv

# Database connection parameters
db_config = {
    'user': 'svbo',
    'password': 'svbopwd',
    'host': 'localhost',
    'database': 'botransactions'
}

def parse_csv(file_path):
    countries_list = []
    with open(file_path, mode='r', encoding='utf8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            country_dict = {
                'id': row[0],
                'ncode': row[1],
                'sname': row[2],
                'fname': row[3],
                'aacode': row[4],
                'aaacode': row[5],
            }
            countries_list.append(country_dict)
    return countries_list


def insert_countries(countries):
    try:
        conn = mysql.connector.connect(**db_config)
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("Connect to DB successful!")

        cursor = conn.cursor()

        total_records = len(countries)
        for i, country in enumerate(countries, 1):

            print(f"Inserting record {i} of {total_records} {country['id']}")

            insert_country_query = """
            INSERT INTO countries (
                id, ncode, sname, fname, aacode, aaacode
            ) VALUES (
                %s, %s, %s, %s, %s, %s
            )
            """
            check_duplicate_query = """
            SELECT id FROM countries WHERE id = %s
            """
            cursor.execute(check_duplicate_query, (country['id'],))
            if cursor.fetchone() is None:
                cursor.execute(insert_country_query, (
                    country['id'], 
                    country['ncode'],
                    country['sname'],
                    country['fname'],
                    country['aacode'],
                    country['aaacode']
                ))
                print(f"Inserted record {i} of {total_records}")
            else:
                print(f"Skipping record {i} of {total_records} due to duplicate id: {country['id']}")

        conn.commit()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python insert_countries.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    print(f"Parsing file: {csv_file}")
    countries = parse_csv(csv_file)
#    print(countries)
    insert_countries(countries)
