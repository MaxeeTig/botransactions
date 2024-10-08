import xml.etree.ElementTree as ET
import mysql.connector
from mysql.connector import errorcode

# Database connection parameters
db_config = {
    'user': 'root',
    'password': 'WYzMP2trak',
    'host': 'localhost',
    'database': 'botransactions'
}


def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespace = {'ns': 'http://sv.bpc.in/SVXP/Operations'}
    operations = []

    for operation in root.findall('ns:operation', namespace):
        operation_data = {
            'oper_id': operation.find('ns:oper_id', namespace).text,
            'oper_type': operation.find('ns:oper_type', namespace).text,
            'msg_type': operation.find('ns:msg_type', namespace).text,
            'sttl_type': operation.find('ns:sttl_type', namespace).text,
            'status': operation.find('ns:status', namespace).text,
            'oper_date': operation.find('ns:oper_date', namespace).text,
            'host_date': operation.find('ns:host_date', namespace).text,
            'oper_amount': {
                'amount_value': operation.find('ns:oper_amount/ns:amount_value', namespace).text,
                'currency': operation.find('ns:oper_amount/ns:currency', namespace).text
            },
            'originator_refnum': operation.find('ns:originator_refnum', namespace).text if operation.find('ns:originator_refnum', namespace) is not None else None,
            'is_reversal': operation.find('ns:is_reversal', namespace).text if operation.find('ns:is_reversal', namespace) is not None else None,
            'merchant_number': operation.find('ns:merchant_number', namespace).text if operation.find('ns:merchant_number', namespace) is not None else None,
            'mcc': operation.find('ns:mcc', namespace).text if operation.find('ns:mcc', namespace) is not None else None,
            'merchant_name': operation.find('ns:merchant_name', namespace).text if operation.find('ns:merchant_name', namespace) is not None else None,
            'merchant_street': operation.find('ns:merchant_street', namespace).text if operation.find('ns:merchant_street', namespace) is not None else None,
            'merchant_city': operation.find('ns:merchant_city', namespace).text if operation.find('ns:merchant_city', namespace) is not None else None,
            'merchant_region': operation.find('ns:merchant_region', namespace).text if operation.find('ns:merchant_region', namespace) is not None else None,
            'merchant_country': operation.find('ns:merchant_country', namespace).text if operation.find('ns:merchant_country', namespace) is not None else None,
            'merchant_postcode': operation.find('ns:merchant_postcode', namespace).text if operation.find('ns:merchant_postcode', namespace) is not None else None,
            'terminal_type': operation.find('ns:terminal_type', namespace).text if operation.find('ns:terminal_type', namespace) is not None else None,
            'terminal_number': operation.find('ns:terminal_number', namespace).text if operation.find('ns:terminal_number', namespace) is not None else None,
            'issuer': {
                'inst_id': operation.find('ns:issuer/ns:inst_id', namespace).text if operation.find('ns:issuer/ns:inst_id', namespace) is not None else None,
                'network_id': operation.find('ns:issuer/ns:network_id', namespace).text if operation.find('ns:issuer/ns:network_id', namespace) is not None else None,
                'card_id': operation.find('ns:issuer/ns:card_id', namespace).text if operation.find('ns:issuer/ns:card_id', namespace) is not None else None,
                'card_instance_id': operation.find('ns:issuer/ns:card_instance_id', namespace).text if operation.find('ns:issuer/ns:card_instance_id', namespace) is not None else None,
                'card_seq_number': operation.find('ns:issuer/ns:card_seq_number', namespace).text if operation.find('ns:issuer/ns:card_seq_number', namespace) is not None else None,
                'card_expir_date': operation.find('ns:issuer/ns:card_expir_date', namespace).text if operation.find('ns:issuer/ns:card_expir_date', namespace) is not None else None,
                'card_country': operation.find('ns:issuer/ns:card_country', namespace).text if operation.find('ns:issuer/ns:card_country', namespace) is not None else None,
                'card_network_id': operation.find('ns:issuer/ns:card_network_id', namespace).text if operation.find('ns:issuer/ns:card_network_id', namespace) is not None else None,
                'auth_code': operation.find('ns:issuer/ns:auth_code', namespace).text if operation.find('ns:issuer/ns:auth_code', namespace) is not None else None
            },
            'acquirer': {
                'inst_id': operation.find('ns:acquirer/ns:inst_id', namespace).text if operation.find('ns:acquirer/ns:inst_id', namespace) is not None else None,
                'network_id': operation.find('ns:acquirer/ns:network_id', namespace).text if operation.find('ns:acquirer/ns:network_id', namespace) is not None else None,
                'merchant_id': operation.find('ns:acquirer/ns:merchant_id', namespace).text if operation.find('ns:acquirer/ns:merchant_id', namespace) is not None else None,
                'terminal_id': operation.find('ns:acquirer/ns:terminal_id', namespace).text if operation.find('ns:acquirer/ns:terminal_id', namespace) is not None else None,
            },
            'transactions': []
        }

        for transaction in operation.findall('ns:transaction', namespace):
            transaction_data = {
                'transaction_id': transaction.find('ns:transaction_id', namespace).text,
                'transaction_type': transaction.find('ns:transaction_type', namespace).text,
                'posting_date': transaction.find('ns:posting_date', namespace).text,
                'debit_entry': {
                    'entry_id': transaction.find('ns:debit_entry/ns:entry_id', namespace).text if transaction.find('ns:debit_entry/ns:entry_id', namespace) is not None else None,
                    'account': {
                        'account_number': transaction.find('ns:debit_entry/ns:account/ns:account_number', namespace).text if transaction.find('ns:debit_entry/ns:account/ns:account_number', namespace) is not None else None,
                        'currency': transaction.find('ns:debit_entry/ns:account/ns:currency', namespace).text if transaction.find('ns:debit_entry/ns:account/ns:currency', namespace) is not None else None
                    },
                    'amount': {
                        'amount_value': transaction.find('ns:debit_entry/ns:amount/ns:amount_value', namespace).text if transaction.find('ns:debit_entry/ns:amount/ns:amount_value', namespace) is not None else None,
                        'currency': transaction.find('ns:debit_entry/ns:amount/ns:currency', namespace).text if transaction.find('ns:debit_entry/ns:amount/ns:currency', namespace) is not None else None
                    }
                },
                'credit_entry': {
                    'entry_id': transaction.find('ns:credit_entry/ns:entry_id', namespace).text if transaction.find('ns:credit_entry/ns:entry_id', namespace) is not None else None,
                    'account': {
                        'account_number': transaction.find('ns:credit_entry/ns:account/ns:account_number', namespace).text if transaction.find('ns:credit_entry/ns:account/ns:account_number', namespace) is not None else None,
                        'currency': transaction.find('ns:credit_entry/ns:account/ns:currency', namespace).text if transaction.find('ns:credit_entry/ns:account/ns:currency', namespace) is not None else None
                    },
                    'amount': {
                        'amount_value': transaction.find('ns:credit_entry/ns:amount/ns:amount_value', namespace).text if transaction.find('ns:credit_entry/ns:amount/ns:amount_value', namespace) is not None else None,
                        'currency': transaction.find('ns:credit_entry/ns:amount/ns:currency', namespace).text if transaction.find('ns:credit_entry/ns:amount/ns:currency', namespace) is not None else None
                    }
                },
                'amount_purpose': transaction.find('ns:amount_purpose', namespace).text if transaction.find('ns:amount_purpose', namespace) is not None else None
            }
            operation_data['transactions'].append(transaction_data)

        operations.append(operation_data)

    return operations

def insert_operations(operations):
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

        total_records = len(operations)
        for i, operation in enumerate(operations, 1):
            if operation['issuer']['card_id'] is None:
                print(f"Skipping record {i} of {total_records} due to empty card_id")
                continue

            print(f"Inserting record {i} of {total_records} {operation['oper_id']}")
            # Insert operation data
            insert_operation_query = """
            INSERT INTO operations (oper_id, oper_type, msg_type, sttl_type, status, oper_date, host_date, amount_value, currency, originator_refnum, is_reversal, merchant_number, mcc, merchant_name, merchant_street, merchant_city, merchant_region, merchant_country, merchant_postcode, terminal_type, terminal_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            check_duplicate_query = """
            SELECT oper_id FROM operations WHERE oper_id = %s
            """
            cursor.execute(check_duplicate_query, (operation['oper_id'],))
            if cursor.fetchone() is None:
                cursor.execute(insert_operation_query, (
                    operation['oper_id'],
                    operation['oper_type'],
                    operation['msg_type'],
                    operation['sttl_type'],
                    operation['status'],
                    operation['oper_date'],
                    operation['host_date'],
                    operation['oper_amount']['amount_value'],
                    operation['oper_amount']['currency'],
                    operation['originator_refnum'],
                    operation['is_reversal'] if operation['is_reversal'] is not None else '0',
                    operation['merchant_number'],
                    operation['mcc'],
                    operation['merchant_name'],
                    operation['merchant_street'],
                    operation['merchant_city'],
                    operation['merchant_region'],
                    operation['merchant_country'],
                    operation['merchant_postcode'],
                    operation['terminal_type'],
                    operation['terminal_number']
                ))
                print(f"Inserted record {i} of {total_records}")
            else:
                print(f"Skipping record {i} of {total_records} due to duplicate oper_id: {operation['oper_id']}")

            # Insert issuer data
            insert_issuer_query = """
            INSERT INTO issuers (oper_id, inst_id, network_id, card_id, card_instance_id, card_seq_number, card_expir_date, card_country, card_network_id, auth_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_issuer_query, (
                operation['oper_id'],
                operation['issuer']['inst_id'] if operation['issuer']['inst_id'] is not None else '1001',
                operation['issuer']['network_id'] if operation['issuer']['network_id'] is not None else '1001',
                operation['issuer']['card_id'],
                operation['issuer']['card_instance_id'],
                operation['issuer']['card_seq_number'] if operation['issuer']['card_seq_number'] is not None else '0',
                operation['issuer']['card_expir_date'] if operation['issuer']['card_expir_date'] is not None else '2025-12-12',
                operation['issuer']['card_country'] if operation['issuer']['card_country'] is not None else '643',
                operation['issuer']['card_network_id'] if operation['issuer']['card_network_id'] is not None else '1001',
                operation['issuer']['auth_code']
            ))
            print(f"Inserted record {i} of {total_records}")

            # Insert acquirer data
            insert_acquirer_query = """
            INSERT INTO acquirers (oper_id, inst_id, network_id, merchant_id, terminal_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_acquirer_query, (
                operation['oper_id'],
                operation['acquirer']['inst_id'],
                operation['acquirer']['network_id'],
                operation['acquirer']['merchant_id'],
                operation['acquirer']['terminal_id']
            ))
            print(f"Inserted record {i} of {total_records}")

            # Insert transaction data
            for transaction in operation['transactions']:
                insert_transaction_query = """
                INSERT INTO transactions (transaction_id, oper_id, transaction_type, posting_date, debit_entry_id, debit_account_number, debit_currency, debit_amount_value, debit_amount_currency, credit_entry_id, credit_account_number, credit_currency, credit_amount_value, credit_amount_currency, amount_purpose)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_transaction_query, (
                    transaction['transaction_id'],
                    operation['oper_id'],
                    transaction['transaction_type'],
                    transaction['posting_date'],
                    transaction['debit_entry']['entry_id'],
                    transaction['debit_entry']['account']['account_number'],
                    transaction['debit_entry']['account']['currency'],
                    transaction['debit_entry']['amount']['amount_value'],
                    transaction['debit_entry']['amount']['currency'],
                    transaction['credit_entry']['entry_id'],
                    transaction['credit_entry']['account']['account_number'],
                    transaction['credit_entry']['account']['currency'],
                    transaction['credit_entry']['amount']['amount_value'],
                    transaction['credit_entry']['amount']['currency'],
                    transaction['amount_purpose']
                ))
                print(f"Inserted record {i} of {total_records}")

        conn.commit()
        cursor.close()
        conn.close()


import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python insert_operations.py <xml_file>")
        sys.exit(1)

    xml_file = sys.argv[1]
    print(f"Parsing file: {xml_file}")
    operations = parse_xml(xml_file)
    insert_operations (operations)
