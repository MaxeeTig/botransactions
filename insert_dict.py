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

def parse_csv(file_path):
    dict_list = []
    with open(file_path, mode='r', encoding='latin1') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            dict_list.append(row)
    return dict_list


def insert_dict(dict_data):
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
        print ("Connect to DB successfull!")

        cursor = conn.cursor()

        total_records = len(dict_data)
        for i, dict_item in enumerate(dict_data, 1):

            print(f"Inserting record {i} of {total_records} {dict_item['id']}")

            insert_dict_query = """
            INSERT INTO dict_table (
                id, dict, code, dkey, text_e, entity_type, is_numeric, is_editable, inst_id, module_code
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            check_duplicate_query = """
            SELECT id FROM dict_table WHERE id = %s
            """
            cursor.execute(check_duplicate_query, (dict_item['id'],))
            if cursor.fetchone() is None:
                    cursor.execute(insert_dict_query, (
                        dict_item['id'], 
                        dict_item['dict'],
                        dict_item['code'],
                        dict_item['dkey'],
                        dict_item['text_e'],
                        dict_item['entity_type'],
                        dict_item['is_numeric'],
                        dict_item['is_editable'],
                        dict_item['inst_id'],
                        dict_item['module_code']
                    ))
                    print(f"Inserted record {i} of {total_records}")
            else:
                print(f"Skipping record {i} of {total_records} due to duplicate id: {dict_item['id']}")

            
        conn.commit()
        cursor.close()
        conn.close()



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python insert_dict.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    print(f"Parsing file: {csv_file}")
    dict_data = parse_csv(csv_file)
    insert_dict(dict_data)
