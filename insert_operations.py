import sys
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


all_tags = [
    'acq_inst_bin', 'acquirer_account_number', 'acquirer_inst_id', 'acquirer_merchant_id', 'acquirer_network_id', 
    'acquirer_terminal_id', 'auth_data_account_cnvt_rate', 'auth_data_acq_device_proc_result', 'auth_data_acq_resp_code', 'auth_data_addl_data', 
    'auth_data_amounts', 'auth_data_atc', 'auth_data_auth_tag', 'auth_data_auth_transaction_id', 'auth_data_bin_amount',
    'auth_data_bin_cnvt_rate', 'auth_data_bin_currency', 'auth_data_card_capture_cap', 'auth_data_card_data_input_cap', 'auth_data_card_data_input_mode',
    'auth_data_card_data_output_cap', 'auth_data_card_presence', 'auth_data_cat_level', 'auth_data_certificate_method', 'auth_data_crdh_auth_cap',
    'auth_data_crdh_auth_entity', 'auth_data_crdh_auth_method', 'auth_data_crdh_presence', 'auth_data_cvr', 'auth_data_cvv2_presence',
    'auth_data_cvv2_result', 'auth_data_device_date', 'auth_data_emv_data', 'auth_data_external_auth_id', 'auth_data_external_orig_id', 
    'auth_data_is_advice', 'auth_data_is_completed', 'auth_data_is_early_emv', 'auth_data_is_repeat', 'auth_data_network_amount', 
    'auth_data_network_cnvt_date', 'auth_data_network_currency', 'auth_data_pin_capture_cap', 'auth_data_pin_presence', 'auth_data_pos_cond_code', 
    'auth_data_pos_entry_mode', 'auth_data_proc_mode', 'auth_data_proc_type', 'auth_data_resp_code', 'auth_data_service_code', 
    'auth_data_terminal_operating_env', 'auth_data_terminal_output_cap', 'auth_data_trace_number', 'auth_data_tvr', 'auth_data_ucaf_indicator', 
    'host_date', 'is_reversal', 'issuer_auth_code', 'issuer_card_country', 'issuer_card_expir_date', 
    'issuer_card_id', 'issuer_card_instance_id', 'issuer_card_network_id', 'issuer_card_number', 'issuer_card_seq_number', 
    'issuer_inst_id', 'issuer_network_id', 'mcc', 'merchant_city', 'merchant_country', 
    'merchant_name', 'merchant_number', 'merchant_postcode', 'merchant_region', 'merchant_street', 
    'msg_type', 'network_refnum', 'oper_amount_amount_value', 'oper_amount_currency', 'oper_date', 
    'oper_id', 'oper_surcharge_amount_amount_value', 'oper_surcharge_amount_currency', 'oper_type', 'original_id', 
    'originator_refnum', 'payment_order_id', 'status', 'sttl_amount_amount_value', 'sttl_amount_currency', 
    'sttl_type', 'terminal_number', 'terminal_type', 'transaction_amount_purpose', 'transaction_conversion_rate',
    'transaction_credit_entry', 'transaction_debit_entry', 'transaction_fee', 'transaction_posting_date', 'transaction_transaction_id',
    'transaction_transaction_type'
]

def parse_xml(file_path):
     tree = ET.parse(file_path)
     root = tree.getroot()
     namespace = {'ns': 'http://sv.bpc.in/SVXP/Operations'}
     operations = []

     for operation in root.findall('.//ns:operation', namespace):
         operation_data = {tag: '' for tag in all_tags}
         for elem in operation:
             if len(elem):
                 for subelem in elem:
                     tag = f"{elem.tag.replace('{http://sv.bpc.in/SVXP/Operations}','')}_{subelem.tag.replace('{http://sv.bpc.in/SVXP/Operations}', '')}"
                     operation_data[tag] = subelem.text
             else:
                 tag = elem.tag.replace('{http://sv.bpc.in/SVXP/Operations}', '')
                 operation_data[tag] = elem.text
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
            # here is set of checking for operations parameters to skip
            if operation['oper)type'] == "OPTP0401":
                print(f"Skipping record {i} of {total_records} due to OPTP0401")
                continue

            print(f"Inserting record {i} of {total_records} {operation['oper_id']}")
            # Insert operation data 5 in line x 20 lines + 1
            insert_operation_query = """
            INSERT INTO operations (
            acq_inst_bin, acquirer_account_number, acquirer_inst_id, acquirer_merchant_id, acquirer_network_id, 
            acquirer_terminal_id, auth_data_account_cnvt_rate, auth_data_acq_device_proc_result, auth_data_acq_resp_code, auth_data_addl_data, 
            auth_data_amounts, auth_data_atc, auth_data_auth_tag, auth_data_auth_transaction_id, auth_data_bin_amount,
            auth_data_bin_cnvt_rate, auth_data_bin_currency, auth_data_card_capture_cap, auth_data_card_data_input_cap, auth_data_card_data_input_mode,
            auth_data_card_data_output_cap, auth_data_card_presence, auth_data_cat_level, auth_data_certificate_method, auth_data_crdh_auth_cap,
            auth_data_crdh_auth_entity, auth_data_crdh_auth_method, auth_data_crdh_presence, auth_data_cvr, auth_data_cvv2_presence,
            auth_data_cvv2_result, auth_data_device_date, auth_data_emv_data, auth_data_external_auth_id, auth_data_external_orig_id, 
            auth_data_is_advice, auth_data_is_completed, auth_data_is_early_emv, auth_data_is_repeat, auth_data_network_amount, 
            auth_data_network_cnvt_date, auth_data_network_currency, auth_data_pin_capture_cap, auth_data_pin_presence, auth_data_pos_cond_code, 
            auth_data_pos_entry_mode, auth_data_proc_mode, auth_data_proc_type, auth_data_resp_code, auth_data_service_code, 
            auth_data_terminal_operating_env, auth_data_terminal_output_cap, auth_data_trace_number, auth_data_tvr, auth_data_ucaf_indicator, 
            host_date, is_reversal, issuer_auth_code, issuer_card_country, issuer_card_expir_date, 
            issuer_card_id, issuer_card_instance_id, issuer_card_network_id, issuer_card_number, issuer_card_seq_number, 
            issuer_inst_id, issuer_network_id, mcc, merchant_city, merchant_country, 
            merchant_name, merchant_number, merchant_postcode, merchant_region, merchant_street, 
            msg_type, network_refnum, oper_amount_amount_value, oper_amount_currency, oper_date, 
            oper_id, oper_surcharge_amount_amount_value, oper_surcharge_amount_currency, oper_type, original_id, 
            originator_refnum, payment_order_id, status, sttl_amount_amount_value, sttl_amount_currency, 
            sttl_type, terminal_number, terminal_type, transaction_amount_purpose, transaction_conversion_rate,
            transaction_credit_entry, transaction_debit_entry, transaction_fee, transaction_posting_date, transaction_transaction_id,
            transaction_transaction_type
            ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s)
            """
            check_duplicate_query = """
            SELECT oper_id FROM operations WHERE oper_id = %s
            """
            cursor.execute(check_duplicate_query, (operation['oper_id'],))
            if cursor.fetchone() is None:
                    cursor.execute(insert_operation_query, (
                        operation['acq_inst_bin'],
                        operation['acquirer_account_number'],
                        operation['acquirer_inst_id'],
                        operation['acquirer_merchant_id'],
                        operation['acquirer_network_id'],
                        operation['acquirer_terminal_id'],
                        operation['auth_data_account_cnvt_rate'],
                        operation['auth_data_acq_device_proc_result'],
                        operation['auth_data_acq_resp_code'],
                        operation['auth_data_addl_data'],
                        operation['auth_data_amounts'],
                        operation['auth_data_atc'],
                        operation['auth_data_auth_tag'],
                        operation['auth_data_auth_transaction_id'],
                        operation['auth_data_bin_amount'],
                        operation['auth_data_bin_cnvt_rate'],
                        operation['auth_data_bin_currency'],
                        operation['auth_data_card_capture_cap'],
                        operation['auth_data_card_data_input_cap'],
                        operation['auth_data_card_data_input_mode'],
                        operation['auth_data_card_data_output_cap'],
                        operation['auth_data_card_presence'],
                        operation['auth_data_cat_level'],
                        operation['auth_data_certificate_method'],
                        operation['auth_data_crdh_auth_cap'],
                        operation['auth_data_crdh_auth_entity'],
                        operation['auth_data_crdh_auth_method'],
                        operation['auth_data_crdh_presence'],
                        operation['auth_data_cvr'],
                        operation['auth_data_cvv2_presence'],
                        operation['auth_data_cvv2_result'],
                        operation['auth_data_device_date'],
                        operation['auth_data_emv_data'],
                        operation['auth_data_external_auth_id'],
                        operation['auth_data_external_orig_id'],
                        operation['auth_data_is_advice'],
                        operation['auth_data_is_completed'],
                        operation['auth_data_is_early_emv'],
                        operation['auth_data_is_repeat'],
                        operation['auth_data_network_amount'],
                        operation['auth_data_network_cnvt_date'],
                        operation['auth_data_network_currency'],
                        operation['auth_data_pin_capture_cap'],
                        operation['auth_data_pin_presence'],
                        operation['auth_data_pos_cond_code'],
                        operation['auth_data_pos_entry_mode'],
                        operation['auth_data_proc_mode'],
                        operation['auth_data_proc_type'],
                        operation['auth_data_resp_code'],
                        operation['auth_data_service_code'],
                        operation['auth_data_terminal_operating_env'],
                        operation['auth_data_terminal_output_cap'],
                        operation['auth_data_trace_number'],
                        operation['auth_data_tvr'],
                        operation['auth_data_ucaf_indicator'],
                        operation['host_date'],
                        operation['is_reversal'],
                        operation['issuer_auth_code'],
                        operation['issuer_card_country'],
                        operation['issuer_card_expir_date'],
                        operation['issuer_card_id'],
                        operation['issuer_card_instance_id'],
                        operation['issuer_card_network_id'],
                        operation['issuer_card_number'],
                        operation['issuer_card_seq_number'],
                        operation['issuer_inst_id'],
                        operation['issuer_network_id'],
                        operation['mcc'],
                        operation['merchant_city'],
                        operation['merchant_country'],
                        operation['merchant_name'],
                        operation['merchant_number'],
                        operation['merchant_postcode'],
                        operation['merchant_region'],
                        operation['merchant_street'],
                        operation['msg_type'],
                        operation['network_refnum'],
                        operation['oper_amount_amount_value'],
                        operation['oper_amount_currency'],
                        operation['oper_date'],
                        operation['oper_id'],
                        operation['oper_surcharge_amount_amount_value'],
                        operation['oper_surcharge_amount_currency'],
                        operation['oper_type'],
                        operation['original_id'],
                        operation['originator_refnum'],
                        operation['payment_order_id'],
                        operation['status'],
                        operation['sttl_amount_amount_value'],
                        operation['sttl_amount_currency'],
                        operation['sttl_type'],
                        operation['terminal_number'],
                        operation['terminal_type'],
                        operation['transaction_amount_purpose'],
                        operation['transaction_conversion_rate'],
                        operation['transaction_credit_entry'],
                        operation['transaction_debit_entry'],
                        operation['transaction_fee'],
                        operation['transaction_posting_date'],
                        operation['transaction_transaction_id'],
                        operation['transaction_transaction_type']
                    ))
                    print(f"Inserted record {i} of {total_records}")
            else:
                print(f"Skipping record {i} of {total_records} due to duplicate oper_id: {operation['oper_id']}")

            
        conn.commit()
        cursor.close()
        conn.close()



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python insert_operations.py <xml_file>")
        sys.exit(1)

    xml_file = sys.argv[1]
    print(f"Parsing file: {xml_file}")
    operations = parse_xml(xml_file)
    insert_operations (operations)
