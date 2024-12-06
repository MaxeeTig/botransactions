import xml.etree.ElementTree as ET
import mysql.connector
from mysql.connector import errorcode
import datetime

# Database connection parameters
db_config = {
    'user': 'svbo',
    'password': 'svbopwd',
    'host': 'localhost',
    'database': 'botransactions'
}

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespace = {'ns': 'http://sv.bpc.in/SVXP/Customers'}
    customers = []

    for customer in root.findall('ns:customer', namespace):
        customer_data = {
            'customer': customer.get('customer_id'),
            'customer_address': customer.find('ns:address', namespace).get('address_id') if customer.find('ns:address', namespace) is not None else None,
            'customer_address_address_name': customer.find('ns:address/ns:address_name', namespace).text if customer.find('ns:address/ns:address_name', namespace) is not None else None,
            'customer_address_address_name_city': customer.find('ns:address/ns:address_name/ns:city', namespace).text if customer.find('ns:address/ns:address_name/ns:city', namespace) is not None else None,
            'customer_address_address_name_comment': customer.find('ns:address/ns:address_name/ns:comment', namespace).text if customer.find('ns:address/ns:address_name/ns:comment', namespace) is not None else None,
            'customer_address_address_name_region': customer.find('ns:address/ns:address_name/ns:region', namespace).text if customer.find('ns:address/ns:address_name/ns:region', namespace) is not None else None,
            'customer_address_address_name_street': customer.find('ns:address/ns:address_name/ns:street', namespace).text if customer.find('ns:address/ns:address_name/ns:street', namespace) is not None else None,
            'customer_address_address_type': customer.find('ns:address/ns:address_type', namespace).text if customer.find('ns:address/ns:address_type', namespace) is not None else None,
            'customer_address_apartment': customer.find('ns:address/ns:apartment', namespace).text if customer.find('ns:address/ns:apartment', namespace) is not None else None,
            'customer_address_country': customer.find('ns:address/ns:country', namespace).text if customer.find('ns:address/ns:country', namespace) is not None else None,
            'customer_address_house': customer.find('ns:address/ns:house', namespace).text if customer.find('ns:address/ns:house', namespace) is not None else None,
            'customer_company': customer.find('ns:company', namespace).get('company_id') if customer.find('ns:company', namespace) is not None else None,
            'customer_company_company_name': customer.find('ns:company/ns:company_name', namespace).text if customer.find('ns:company/ns:company_name', namespace) is not None else None,
            'customer_company_company_name_company_full_name': customer.find('ns:company/ns:company_name/ns:company_full_name', namespace).text if customer.find('ns:company/ns:company_name/ns:company_full_name', namespace) is not None else None,
            'customer_company_company_name_company_short_name': customer.find('ns:company/ns:company_name/ns:company_short_name', namespace).text if customer.find('ns:company/ns:company_name/ns:company_short_name', namespace) is not None else None,
            'customer_company_embossed_name': customer.find('ns:company/ns:embossed_name', namespace).text if customer.find('ns:company/ns:embossed_name', namespace) is not None else None,
            'customer_company_identity_card': customer.find('ns:company/ns:identity_card', namespace).get('identity_card_id') if customer.find('ns:company/ns:identity_card', namespace) is not None else None,
            'customer_company_identity_card_id_issue_date': customer.find('ns:company/ns:identity_card/ns:id_issue_date', namespace).text if customer.find('ns:company/ns:identity_card/ns:id_issue_date', namespace) is not None else None,
            'customer_company_identity_card_id_number': customer.find('ns:company/ns:identity_card/ns:id_number', namespace).text if customer.find('ns:company/ns:identity_card/ns:id_number', namespace) is not None else None,
            'customer_company_identity_card_id_series': customer.find('ns:company/ns:identity_card/ns:id_series', namespace).text if customer.find('ns:company/ns:identity_card/ns:id_series', namespace) is not None else None,
            'customer_company_identity_card_id_type': customer.find('ns:company/ns:identity_card/ns:id_type', namespace).text if customer.find('ns:company/ns:identity_card/ns:id_type', namespace) is not None else None,
            'customer_company_incorp_form': customer.find('ns:company/ns:incorp_form', namespace).text if customer.find('ns:company/ns:incorp_form', namespace) is not None else None,
            'customer_contact': customer.find('ns:contact', namespace).get('contact_id') if customer.find('ns:contact', namespace) is not None else None,
            'customer_contact_contact_data': customer.find('ns:contact/ns:contact_data', namespace).text if customer.find('ns:contact/ns:contact_data', namespace) is not None else None,
            'customer_contact_contact_data_commun_address': customer.find('ns:contact/ns:contact_data/ns:commun_address', namespace).text if customer.find('ns:contact/ns:contact_data/ns:commun_address', namespace) is not None else None,
            'customer_contact_contact_data_commun_method': customer.find('ns:contact/ns:contact_data/ns:commun_method', namespace).text if customer.find('ns:contact/ns:contact_data/ns:commun_method', namespace) is not None else None,
            'customer_contact_contact_data_start_date': customer.find('ns:contact/ns:contact_data/ns:start_date', namespace).text if customer.find('ns:contact/ns:contact_data/ns:start_date', namespace) is not None else None,
            'customer_contact_contact_type': customer.find('ns:contact/ns:contact_type', namespace).text if customer.find('ns:contact/ns:contact_type', namespace) is not None else None,
            'customer_contact_job_title': customer.find('ns:contact/ns:job_title', namespace).text if customer.find('ns:contact/ns:job_title', namespace) is not None else None,
            'customer_contact_person': customer.find('ns:contact/ns:person', namespace).get('person_id') if customer.find('ns:contact/ns:person', namespace) is not None else None,
            'customer_contact_person_identity_card': customer.find('ns:contact/ns:person/ns:identity_card', namespace).get('identity_card_id') if customer.find('ns:contact/ns:person/ns:identity_card', namespace) is not None else None,
            'customer_contact_person_identity_card_id_number': customer.find('ns:contact/ns:person/ns:identity_card/ns:id_number', namespace).text if customer.find('ns:contact/ns:person/ns:identity_card/ns:id_number', namespace) is not None else None,
            'customer_contact_person_identity_card_id_series': customer.find('ns:contact/ns:person/ns:identity_card/ns:id_series', namespace).text if customer.find('ns:contact/ns:person/ns:identity_card/ns:id_series', namespace) is not None else None,
            'customer_contact_person_identity_card_id_type': customer.find('ns:contact/ns:person/ns:identity_card/ns:id_type', namespace).text if customer.find('ns:contact/ns:person/ns:identity_card/ns:id_type', namespace) is not None else None,
            'customer_contact_person_person_name': customer.find('ns:contact/ns:person/ns:person_name', namespace).text if customer.find('ns:contact/ns:person/ns:person_name', namespace) is not None else None,
            'customer_contact_person_person_name_first_name': customer.find('ns:contact/ns:person/ns:person_name/ns:first_name', namespace).text if customer.find('ns:contact/ns:person/ns:person_name/ns:first_name', namespace) is not None else None,
            'customer_contact_person_person_name_second_name': customer.find('ns:contact/ns:person/ns:person_name/ns:second_name', namespace).text if customer.find('ns:contact/ns:person/ns:person_name/ns:second_name', namespace) is not None else None,
            'customer_contact_person_person_name_surname': customer.find('ns:contact/ns:person/ns:person_name/ns:surname', namespace).text if customer.find('ns:contact/ns:person/ns:person_name/ns:surname', namespace) is not None else None,
            'customer_contact_preferred_lang': customer.find('ns:contact/ns:preferred_lang', namespace).text if customer.find('ns:contact/ns:preferred_lang', namespace) is not None else None,
            'customer_contract': customer.find('ns:contract', namespace).get('contract_id') if customer.find('ns:contract', namespace) is not None else None,
            'customer_contract_agent_id': customer.find('ns:contract/ns:agent_id', namespace).text if customer.find('ns:contract/ns:agent_id', namespace) is not None else None,
            'customer_contract_agent_number': customer.find('ns:contract/ns:agent_number', namespace).text if customer.find('ns:contract/ns:agent_number', namespace) is not None else None,
            'customer_contract_contract_number': customer.find('ns:contract/ns:contract_number', namespace).text if customer.find('ns:contract/ns:contract_number', namespace) is not None else None,
            'customer_contract_contract_type': customer.find('ns:contract/ns:contract_type', namespace).text if customer.find('ns:contract/ns:contract_type', namespace) is not None else None,
            'customer_contract_end_date': customer.find('ns:contract/ns:end_date', namespace).text if customer.find('ns:contract/ns:end_date', namespace) is not None else None,
            'customer_contract_product_id': customer.find('ns:contract/ns:product_id', namespace).text if customer.find('ns:contract/ns:product_id', namespace) is not None else None,
            'customer_contract_product_number': customer.find('ns:contract/ns:product_number', namespace).text if customer.find('ns:contract/ns:product_number', namespace) is not None else None,
            'customer_contract_start_date': customer.find('ns:contract/ns:start_date', namespace).text if customer.find('ns:contract/ns:start_date', namespace) is not None else None,
            'customer_customer_category': customer.find('ns:customer_category', namespace).text if customer.find('ns:customer_category', namespace) is not None else None,
            'customer_customer_ext_id': customer.find('ns:customer_ext_id', namespace).text if customer.find('ns:customer_ext_id', namespace) is not None else None,
            'customer_customer_ext_type': customer.find('ns:customer_ext_type', namespace).text if customer.find('ns:customer_ext_type', namespace) is not None else None,
            'customer_customer_number': customer.find('ns:customer_number', namespace).text if customer.find('ns:customer_number', namespace) is not None else None,
            'customer_customer_relation': customer.find('ns:customer_relation', namespace).text if customer.find('ns:customer_relation', namespace) is not None else None,
            'customer_inst_id': customer.find('ns:inst_id', namespace).text if customer.find('ns:inst_id', namespace) is not None else None,
            'customer_money_laundry_reason': customer.find('ns:money_laundry_reason', namespace).text if customer.find('ns:money_laundry_reason', namespace) is not None else None,
            'customer_money_laundry_risk': customer.find('ns:money_laundry_risk', namespace).text if customer.find('ns:money_laundry_risk', namespace) is not None else None,
            'customer_nationality': customer.find('ns:nationality', namespace).text if customer.find('ns:nationality', namespace) is not None else None,
            'customer_note': customer.find('ns:note', namespace).get('note_id') if customer.find('ns:note', namespace) is not None else None,
            'customer_note_note_content': customer.find('ns:note/ns:note_content', namespace).text if customer.find('ns:note/ns:note_content', namespace) is not None else None,
            'customer_note_note_content_note_header': customer.find('ns:note/ns:note_content/ns:note_header', namespace).text if customer.find('ns:note/ns:note_content/ns:note_header', namespace) is not None else None,
            'customer_note_note_content_note_text': customer.find('ns:note/ns:note_content/ns:note_text', namespace).text if customer.find('ns:note/ns:note_content/ns:note_text', namespace) is not None else None,
            'customer_note_note_type': customer.find('ns:note/ns:note_type', namespace).text if customer.find('ns:note/ns:note_type', namespace) is not None else None,
            'customer_person': customer.find('ns:person', namespace).get('person_id') if customer.find('ns:person', namespace) is not None else None,
            'customer_person_birthday': customer.find('ns:person/ns:birthday', namespace).text if customer.find('ns:person/ns:birthday', namespace) is not None else None,
            'customer_person_gender': customer.find('ns:person/ns:gender', namespace).text if customer.find('ns:person/ns:gender', namespace) is not None else None,
            'customer_person_identity_card': customer.find('ns:person/ns:identity_card', namespace).get('identity_card_id') if customer.find('ns:person/ns:identity_card', namespace) is not None else None,
            'customer_person_identity_card_id_issuer': customer.find('ns:person/ns:identity_card/ns:id_issuer', namespace).text if customer.find('ns:person/ns:identity_card/ns:id_issuer', namespace) is not None else None,
            'customer_person_identity_card_id_number': customer.find('ns:person/ns:identity_card/ns:id_number', namespace).text if customer.find('ns:person/ns:identity_card/ns:id_number', namespace) is not None else None,
            'customer_person_identity_card_id_series': customer.find('ns:person/ns:identity_card/ns:id_series', namespace).text if customer.find('ns:person/ns:identity_card/ns:id_series', namespace) is not None else None,
            'customer_person_identity_card_id_type': customer.find('ns:person/ns:identity_card/ns:id_type', namespace).text if customer.find('ns:person/ns:identity_card/ns:id_type', namespace) is not None else None,
            'customer_person_person_name': customer.find('ns:person/ns:person_name', namespace).text if customer.find('ns:person/ns:person_name', namespace) is not None else None,
            'customer_person_person_name_first_name': customer.find('ns:person/ns:person_name/ns:first_name', namespace).text if customer.find('ns:person/ns:person_name/ns:first_name', namespace) is not None else None,
            'customer_person_person_name_second_name': customer.find('ns:person/ns:person_name/ns:second_name', namespace).text if customer.find('ns:person/ns:person_name/ns:second_name', namespace) is not None else None,
            'customer_person_person_name_surname': customer.find('ns:person/ns:person_name/ns:surname', namespace).text if customer.find('ns:person/ns:person_name/ns:surname', namespace) is not None else None,
            'customer_person_person_title': customer.find('ns:person/ns:person_title', namespace).text if customer.find('ns:person/ns:person_title', namespace) is not None else None,
            'customer_person_place_of_birth': customer.find('ns:person/ns:place_of_birth', namespace).text if customer.find('ns:person/ns:place_of_birth', namespace) is not None else None,
            'customer_person_suffix': customer.find('ns:person/ns:suffix', namespace).text if customer.find('ns:person/ns:suffix', namespace) is not None else None,
            'customer_resident': customer.find('ns:resident', namespace).text if customer.find('ns:resident', namespace) is not None else None,
            'customer_status': customer.find('ns:status', namespace).text if customer.find('ns:status', namespace) is not None else None,
            'file_id': customer.find('ns:file_id', namespace).text if customer.find('ns:file_id', namespace) is not None else None,
            'file_type': customer.find('ns:file_type', namespace).text if customer.find('ns:file_type', namespace) is not None else None,
            'inst_id': customer.find('ns:inst_id', namespace).text if customer.find('ns:inst_id', namespace) is not None else None,
        }
        customers.append(customer_data)

    return customers

def insert_customers(customers):
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

        total_records = len(customers)
        for i, customer in enumerate(customers, 1):
            print(f"Inserting record {i} of {total_records}")

            # Check if customer exists
            check_customer_query = """
            SELECT customer FROM customers WHERE customer = %s
            """
            cursor.execute(check_customer_query, (customer['customer'],))
            existing_customer = cursor.fetchone()

            if existing_customer is None:
                # Insert customer data
                insert_customer_query = """INSERT INTO customers (
                    customer, customer_address, customer_address_address_name, customer_address_address_name_city, 
                    customer_address_address_name_comment, customer_address_address_name_region, customer_address_address_name_street, customer_address_address_type, 
                    customer_address_apartment, customer_address_country, customer_address_house, customer_company, 
                    customer_company_company_name, customer_company_company_name_company_full_name, customer_company_company_name_company_short_name, customer_company_embossed_name, 
                    customer_company_identity_card, customer_company_identity_card_id_issue_date, customer_company_identity_card_id_number, customer_company_identity_card_id_series,
                    customer_company_identity_card_id_type, customer_company_incorp_form, customer_contact, customer_contact_contact_data,
                    customer_contact_contact_data_commun_address, customer_contact_contact_data_commun_method, customer_contact_contact_data_start_date, customer_contact_contact_type, 
                    customer_contact_job_title, customer_contact_person, customer_contact_person_identity_card, customer_contact_person_identity_card_id_number, 
                    customer_contact_person_identity_card_id_series, customer_contact_person_identity_card_id_type, customer_contact_person_person_name, customer_contact_person_person_name_first_name,
                    customer_contact_person_person_name_second_name, customer_contact_person_person_name_surname, customer_contact_preferred_lang, customer_contract, 
                    customer_contract_agent_id,  customer_contract_agent_number, customer_contract_contract_number, customer_contract_contract_type, 
                    customer_contract_end_date, customer_contract_product_id, customer_contract_product_number, customer_contract_start_date, 
                    customer_customer_category, customer_customer_ext_id, customer_customer_ext_type, customer_customer_number, 
                    customer_customer_relation, customer_inst_id, customer_money_laundry_reason, customer_money_laundry_risk, 
                    customer_nationality, customer_note, customer_note_note_content, customer_note_note_content_note_header, 
                    customer_note_note_content_note_text, customer_note_note_type, customer_person, customer_person_birthday, 
                    customer_person_gender, customer_person_identity_card, customer_person_identity_card_id_issuer, customer_person_identity_card_id_number, 
                    customer_person_identity_card_id_series, customer_person_identity_card_id_type, customer_person_person_name, customer_person_person_name_first_name, 
                    customer_person_person_name_second_name, customer_person_person_name_surname, customer_person_person_title, customer_person_place_of_birth, 
                    customer_person_suffix, customer_resident, customer_status, file_id, 
                    file_type, inst_id
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s)
                    """
