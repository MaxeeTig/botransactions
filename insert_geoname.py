import sys
import mysql.connector
from mysql.connector import errorcode

# Database connection parameters
db_config = {
    'user': 'svbo',
    'password': 'svbopwd',
    'host': 'localhost',
    'database': 'botransactions'
}

import csv

def parse_tab_file(file_path):
    geoname_list = []
    with open(file_path, mode='r', encoding='utf8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            geoname_dict = {
                'geonameid': row[0],
                'name': row[1],
                'asciiname': row[2],
                'alternatenames': row[3],
                'country_code': row[8]
            }
            geoname_list.append(geoname_dict)
    return geoname_list


def insert_geoname(geoname):
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
        print ("Connect to DB successful!")

        cursor = conn.cursor()

        total_records = len(geoname)
        for i, geoname in enumerate(geoname, 1):

            print(f"Inserting record {i} of {total_records} {geoname['geonameid']}")

            insert_geoname_query = """
            INSERT INTO geoname (
                geonameid, name, asciiname, alternatenames, country_code
            ) VALUES (
                %s, %s, %s, %s, %s)
            """
            check_duplicate_query = """
            SELECT geonameid FROM geoname WHERE geonameid = %s
            """
            cursor.execute(check_duplicate_query, (geoname['geonameid'],))
            if cursor.fetchone() is None:
                    cursor.execute(insert_geoname_query, (
                        geoname['geonameid'],
                        geoname['name'],
                        geoname['asciiname'],
                        geoname['alternatenames'].encode('utf-8').decode('utf-8'),
                        geoname['country_code']
                    ))
                    print(f"Inserted record {i} of {total_records}")
            else:
                print(f"Skipping record {i} of {total_records} due to duplicate geonameid: {geoname['geonameid']}")


        conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python insert_geoname.py <tab_file>")
        sys.exit(1)

    tab_file = sys.argv[1]
    print(f"Parsing file: {tab_file}")
    geoname = parse_tab_file(tab_file)
    insert_geoname(geoname)
