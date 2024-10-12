import sys
import mysql.connector
from mysql.connector import errorcode

# Database connection parameters
db_config = {
    'user': 'root',
    'password': 'WYzMP2trak',
    'host': 'localhost',
    'database': 'botransactions'
}

import csv

def parse_csv(file_path):
    dict_list = []
    with open(file_path, mode='r', encoding='utf-8') as file:
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

            print(f"Inserting record {i} of {total_records} {dict_item['ID']}")

            insert_dict_query = """
            INSERT INTO dict_table (
                ID, DICT, CODE, KEY, TEXT_E, ENTITY_TYPE, IS_NUMERIC, IS_EDITABLE, INST_ID, MODULE_CODE
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            check_duplicate_query = """
            SELECT ID FROM dict_table WHERE ID = %s
            """
            cursor.execute(check_duplicate_query, (dict_item['ID'],))
            if cursor.fetchone() is None:
                    cursor.execute(insert_dict_query, (
                        dict_item['ID'], 
                        dict_item['DICT'],
                        dict_item['CODE'],
                        dict_item['KEY'],
                        dict_item['TEXT_E'],
                        dict_item['ENTITY_TYPE'],
                        dict_item['IS_NUMERIC'],
                        dict_item['IS_EDITABLE'],
                        dict_item['INST_ID'],
                        dict_item['MODULE_CODE']
                    ))
                    print(f"Inserted record {i} of {total_records}")
            else:
                print(f"Skipping record {i} of {total_records} due to duplicate ID: {dict_item['ID']}")

            
        conn.commit()
        cursor.close()
        conn.close()



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python insert_mcc.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    print(f"Parsing file: {csv_file}")
    dict_data = parse_csv(csv_file)
    insert_dict(dict_data)
