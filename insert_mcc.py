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


all_tags = [
    'mcc', 'edited_description','combined_description','usda_description','irs_description','irs_reportable'
]

import csv

def parse_csv(file_path):
    mcc_list = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            mcc_list.append(row)
    return mcc_list


def insert_mcc(mcc):
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

        total_records = len(mcc)
        for i, mcc in enumerate(mcc, 1):

            print(f"Inserting record {i} of {total_records} {mcc['mcc']}")

            insert_mcc_query = """
            INSERT INTO mcc (
		mcc, edited_description, combined_description, usda_description, irs_description, irs_reportable
            ) VALUES (
            %s, %s, %s, %s, %s, %s)
            """
            check_duplicate_query = """
            SELECT mcc FROM mcc WHERE mcc = %s
            """
            cursor.execute(check_duplicate_query, (mcc['mcc'],))
            if cursor.fetchone() is None:
                    cursor.execute(insert_mcc_query, (
			mcc['mcc'], 
			mcc['edited_description'],
			mcc['combined_description'],
			mcc['usda_description'],
			mcc['irs_description'],
			mcc['irs_reportable']
                    ))
                    print(f"Inserted record {i} of {total_records}")
            else:
                print(f"Skipping record {i} of {total_records} due to duplicate mcc: {mcc['mcc']}")

            
        conn.commit()
        cursor.close()
        conn.close()



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python insert_mcc.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    print(f"Parsing file: {csv_file}")
    mcc = parse_csv(csv_file)
    insert_mcc(mcc)
