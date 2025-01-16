# import cards script #
import xml.etree.ElementTree as ET
import mysql.connector
from mysql.connector import errorcode

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
    namespace = {'ns': 'http://sv.bpc.in/SVXP/Cards'}
    cards = []

    for card in root.findall('ns:card', namespace):
        card_data = {
            'card_id': card.get('card_id'),
            'inst_id': card.find('ns:inst_id', namespace).text if card.find('ns:inst_id', namespace) is not None else None,
            'card_number': card.find('ns:card_number', namespace).text if card.find('ns:card_number', namespace) is not None else None,
            'card_mask': card.find('ns:card_mask', namespace).text if card.find('ns:card_mask', namespace) is not None else card.find('ns:card_number', namespace).text,  # Provide a default value
            'card_type': card.find('ns:card_type', namespace).text if card.find('ns:card_type', namespace) is not None else None,
            'country': card.find('ns:country', namespace).text if card.find('ns:country', namespace) is not None else None,
            'category': card.find('ns:category', namespace).text if card.find('ns:category', namespace) is not None else None,
            'reg_date': card.find('ns:reg_date', namespace).text if card.find('ns:reg_date', namespace) is not None else None,
            'customer': {
                'customer_id': card.find('ns:customer', namespace).get('customer_id')
            },
            'contract': {
                'contract_id': card.find('ns:contract', namespace).get('contract_id')
            },
            'cardholder': {
                'cardholder_id': card.find('ns:cardholder', namespace).get('cardholder_id'),
                'cardholder_number': card.find('ns:cardholder/ns:cardholder_number', namespace).text if card.find('ns:cardholder/ns:cardholder_number', namespace) is not None else None,
                'cardholder_name': card.find('ns:cardholder/ns:cardholder_name', namespace).text if card.find('ns:cardholder/ns:cardholder_name', namespace) is not None else None,
                'person': {
                    'person_id': card.find('ns:cardholder/ns:person', namespace).get('person_id') if card.find('ns:cardholder/ns:person', namespace) is not None else None,
                    'surname': card.find('ns:cardholder/ns:person/ns:person_name/ns:surname', namespace).text if card.find('ns:cardholder/ns:person/ns:person_name/ns:surname', namespace) is not None else None,
                    'first_name': card.find('ns:cardholder/ns:person/ns:person_name/ns:first_name', namespace).text if card.find('ns:cardholder/ns:person/ns:person_name/ns:first_name', namespace) is not None else None,
                    'identity_card': {
                        'id_type': card.find('ns:cardholder/ns:person/ns:identity_card/ns:id_type', namespace).text if card.find('ns:cardholder/ns:person/ns:identity_card/ns:id_type', namespace) is not None else 'IDTP0001',  # Provide a default value
                        'id_series': card.find('ns:cardholder/ns:person/ns:identity_card/ns:id_series', namespace).text if card.find('ns:cardholder/ns:person/ns:identity_card/ns:id_series', namespace) is not None else None,
                        'id_number': card.find('ns:cardholder/ns:person/ns:identity_card/ns:id_number', namespace).text if card.find('ns:cardholder/ns:person/ns:identity_card/ns:id_number', namespace) is not None else None
                    }
                },
                'address': {
                    'address_id': card.find('ns:cardholder/ns:address', namespace).get('address_id') if card.find('ns:cardholder/ns:address', namespace) is not None else None,
                    'address_type': card.find('ns:cardholder/ns:address/ns:address_type', namespace).text if card.find('ns:cardholder/ns:address/ns:address_type', namespace) is not None else None,
                    'country': card.find('ns:cardholder/ns:address/ns:country', namespace).text if card.find('ns:cardholder/ns:address/ns:country', namespace) is not None else None,
                    'region': card.find('ns:cardholder/ns:address/ns:address_name/ns:region', namespace).text if card.find('ns:cardholder/ns:address/ns:address_name/ns:region', namespace) is not None else None,
                    'city': card.find('ns:cardholder/ns:address/ns:address_name/ns:city', namespace).text if card.find('ns:cardholder/ns:address/ns:address_name/ns:city', namespace) is not None else None,
                    'street': card.find('ns:cardholder/ns:address/ns:address_name/ns:street', namespace).text if card.find('ns:cardholder/ns:address/ns:address_name/ns:street', namespace) is not None else None,
                    'house': card.find('ns:cardholder/ns:address/ns:house', namespace).text if card.find('ns:cardholder/ns:address/ns:house', namespace) is not None else None,
                    'postal_code': card.find('ns:cardholder/ns:address/ns:postal_code', namespace).text if card.find('ns:cardholder/ns:address/ns:postal_code', namespace) is not None else None
                }
            },
            'card_instance': {
                'instance_id': card.find('ns:card_instance', namespace).get('instance_id'),
                'inst_id': card.find('ns:card_instance/ns:inst_id', namespace).text if card.find('ns:card_instance/ns:inst_id', namespace) is not None else None,
                'agent_id': card.find('ns:card_instance/ns:agent_id', namespace).text if card.find('ns:card_instance/ns:agent_id', namespace) is not None else None,
                'agent_number': card.find('ns:card_instance/ns:agent_number', namespace).text if card.find('ns:card_instance/ns:agent_number', namespace) is not None else None,
                'sequential_number': card.find('ns:card_instance/ns:sequential_number', namespace).text if card.find('ns:card_instance/ns:sequential_number', namespace) is not None else None,
                'card_status': card.find('ns:card_instance/ns:card_status', namespace).text if card.find('ns:card_instance/ns:card_status', namespace) is not None else None,
                'card_state': card.find('ns:card_instance/ns:card_state', namespace).text if card.find('ns:card_instance/ns:card_state', namespace) is not None else None,
                'iss_date': card.find('ns:card_instance/ns:iss_date', namespace).text if card.find('ns:card_instance/ns:iss_date', namespace) is not None else "2013-08-03",  # Provide a default value
                'start_date': card.find('ns:card_instance/ns:start_date', namespace).text if card.find('ns:card_instance/ns:start_date', namespace) is not None else None,
                'expiration_date': card.find('ns:card_instance/ns:expiration_date', namespace).text if card.find('ns:card_instance/ns:expiration_date', namespace) is not None else None,
                'pin_update_flag': card.find('ns:card_instance/ns:pin_update_flag', namespace).text if card.find('ns:card_instance/ns:pin_update_flag', namespace) is not None else None,
                'pin_request': card.find('ns:card_instance/ns:pin_request', namespace).text if card.find('ns:card_instance/ns:pin_request', namespace) is not None else None,
                'perso_priority': card.find('ns:card_instance/ns:perso_priority', namespace).text if card.find('ns:card_instance/ns:perso_priority', namespace) is not None else None,
                'embossing_request': card.find('ns:card_instance/ns:embossing_request', namespace).text if card.find('ns:card_instance/ns:embossing_request', namespace) is not None else None,
                'pin_mailer_request': card.find('ns:card_instance/ns:pin_mailer_request', namespace).text if card.find('ns:card_instance/ns:pin_mailer_request', namespace) is not None else None
            },
            'account': {
                'account_id': card.find('ns:account', namespace).get('account_id') if card.find('ns:account', namespace) is not None else None,
                'account_number': card.find('ns:account/ns:account_number', namespace).text if card.find('ns:account/ns:account_number', namespace) is not None else None,
                'account_type': card.find('ns:account/ns:account_type', namespace).text if card.find('ns:account/ns:account_type', namespace) is not None else None,
                'currency': card.find('ns:account/ns:currency', namespace).text if card.find('ns:account/ns:currency', namespace) is not None else None,
                'account_status': card.find('ns:account/ns:account_status', namespace).text if card.find('ns:account/ns:account_status', namespace) is not None else None,
                'link_flag': card.find('ns:account/ns:link_flag', namespace).text if card.find('ns:account/ns:link_flag', namespace) is not None else None
            }
        }

        cards.append(card_data)

    return cards

def insert_cards(cards):
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

        total_records = len(cards)
        for i, card in enumerate(cards, 1):
            print(f"Inserting record {i} of {total_records} {card['customer']['customer_id']}")
            # Insert card data
            insert_card_query = """
            INSERT INTO cards (card_id, inst_id, card_number, card_mask, card_type, country, category, reg_date, customer_id, contract_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_card_query, (
                card['card_id'],
                card['inst_id'],
                card['card_number'],
                card['card_mask'] if card['card_mask'] is not None else 'default_mask',  # Provide a default value
                card['card_type'],
                card['country'],
                card['category'],
                card['reg_date'],
                card['customer']['customer_id'],
                card['contract']['contract_id']
            ))
            print(f"Inserted record {i} of {total_records}")

            # Check if person_id exists
            if card['cardholder']['person']['person_id'] is not None:
                # Check if person_id exists in persons table
                check_person_query = """
                SELECT person_id FROM persons WHERE person_id = %s
                """
                cursor.execute(check_person_query, (card['cardholder']['person']['person_id'],))
                person_exists = cursor.fetchone()

                if not person_exists:
                    if card['customer']['customer_id'] is not None:
                        # Insert person data
                        insert_person_query = """
                        INSERT INTO persons (person_id, surname, first_name, id_type, id_series, id_number, customer_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(insert_person_query, (
                            card['cardholder']['person']['person_id'],
                            card['cardholder']['person']['surname'],
                            card['cardholder']['person']['first_name'],
                            card['cardholder']['person']['identity_card']['id_type'],
                            card['cardholder']['person']['identity_card']['id_series'],
                            card['cardholder']['person']['identity_card']['id_number'],
                            card['customer']['customer_id']  # Ensure customer_id is included
                        ))
                        print(f"Inserted person record {i} of {total_records}")
                    else:
                        print(f"Skipped person record {i} of {total_records} due to missing customer_id")

            # Check if address_id exists
            check_address_query = """
            SELECT address_id FROM addresses WHERE address_id = %s
            """
            cursor.execute(check_address_query, (card['cardholder']['address']['address_id'],))
            address_exists = cursor.fetchone()

            if not address_exists:
                if card['cardholder']['address']['address_id'] is not None:
                    # Insert address data
                    if card['customer']['customer_id'] is not None:
                        insert_address_query = """
                        INSERT INTO addresses (address_id, address_type, country, region, city, street, house, postal_code, customer_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(insert_address_query, (
                            card['cardholder']['address']['address_id'],
                            card['cardholder']['address']['address_type'] if card['cardholder']['address']['address_type'] is not None else "ADPTHOME",
                            card['cardholder']['address']['country'],
                            card['cardholder']['address']['region'] if card['cardholder']['address']['region'] is not None else 'default_region',  # Provide a default value
                            card['cardholder']['address']['city'] if card['cardholder']['address']['city'] is not None else 'NONE',
                            card['cardholder']['address']['street'] if card['cardholder']['address']['street'] is not None else 'NONE',
                            card['cardholder']['address']['house'] if card['cardholder']['address']['house'] is not None else 'NONE',
                            card['cardholder']['address']['postal_code'] if card['cardholder']['address']['postal_code'] is not None else '111111',
                            card['customer']['customer_id']  # Ensure customer_id is included
                        ))
                        print(f"Inserted address record {i} of {total_records}")
                    else:
                        print(f"Skipped address record {i} of {total_records} due to missing customer_id")

            # Insert cardholder data
            if card['cardholder']['person']['person_id'] is not None and card['cardholder']['address']['address_id'] is not None:
                # Check if cardholder_id exists in cardholders table
                check_cardholder_query = """
                SELECT cardholder_id FROM cardholders WHERE cardholder_id = %s
                """
                cursor.execute(check_cardholder_query, (card['cardholder']['cardholder_id'],))
                cardholder_exists = cursor.fetchone()

                if not cardholder_exists:
                    insert_cardholder_query = """
                    INSERT INTO cardholders (cardholder_id, card_id, cardholder_number, cardholder_name, person_id, address_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_cardholder_query, (
                        card['cardholder']['cardholder_id'],
                        card['card_id'],
                        card['cardholder']['cardholder_number'],
                        card['cardholder']['cardholder_name'] if card['cardholder']['cardholder_name'] is not None else 'Default CH name',  # Provide a default value
                        card['cardholder']['person']['person_id'],
                        card['cardholder']['address']['address_id']
                    ))
                    print(f"Inserted cardholder record {i} of {total_records}")
                else:
                    print(f"Skipped cardholder record {i} of {total_records} due to duplicate cardholder_id")
            else:
                if card['cardholder']['person']['person_id'] is None:
                    print(f"Skipped cardholder record {i} of {total_records} due to missing person_id")
                if card['cardholder']['address']['address_id'] is None:
                    print(f"Skipped cardholder record {i} of {total_records} due to missing address_id")

            # Insert card instance data
            insert_card_instance_query = """
            INSERT INTO card_instances (instance_id, card_id, inst_id, agent_id, agent_number, sequential_number, card_status, card_state, iss_date, start_date, expiration_date, pin_update_flag, pin_request, perso_priority, embossing_request, pin_mailer_request)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_card_instance_query, (
                card['card_instance']['instance_id'],
                card['card_id'],
                card['card_instance']['inst_id'],
                card['card_instance']['agent_id'],
                card['card_instance']['agent_number'],
                card['card_instance']['sequential_number'] if card['card_instance']['sequential_number'] is not None else '0',  # Provide a default value,
                card['card_instance']['card_status'] if card['card_instance']['card_status'] is not None else 'CSTS0000',  # Provide a default value
                card['card_instance']['card_state'] if card['card_instance']['card_state'] is not None else 'CSTE0200',  # Provide a default value
                card['card_instance']['iss_date'],
                card['card_instance']['start_date'] if card['card_instance']['start_date'] is not None else '2013-08-03',
                card['card_instance']['expiration_date'] if card['card_instance']['expiration_date'] is not None else '2025-01-01',
                card['card_instance']['pin_update_flag'],
                card['card_instance']['pin_request'],
                card['card_instance']['perso_priority'],
                card['card_instance']['embossing_request'],
                card['card_instance']['pin_mailer_request']
            ))
            print(f"Inserted record {i} of {total_records}")

            # Check if account_id exists
            if card['account']['account_id'] is not None:
                # Check if account_id exists in accounts table
                check_account_query = """
                SELECT account_id FROM accounts WHERE account_id = %s
                """
                cursor.execute(check_account_query, (card['account']['account_id'],))
                account_exists = cursor.fetchone()

                if not account_exists:
                    # Insert account data
                    insert_account_query = """
                    INSERT INTO accounts (account_id, card_id, account_number, account_type, currency, account_status, link_flag)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_account_query, (
                        card['account']['account_id'],
                        card['card_id'],
                        card['account']['account_number'],
                        card['account']['account_type'],
                        card['account']['currency'] if card['account']['currency'] is not None else '643',  # Provide a default value
                        card['account']['account_status'] if card['account']['account_status'] is not None else 'ACSTACTV',  # Provide a default value,ACSTACTV
                        card['account']['link_flag']
                    ))
                    print(f"Inserted record {i} of {total_records}")
                else:
                    print(f"Skipped account record {i} of {total_records} due to duplicate account_id")
            else:
                print(f"Skipped account record {i} of {total_records} due to missing account_id")

        conn.commit()
        cursor.close()
        conn.close()

import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python insert_cards.py <xml_file>")
        sys.exit(1)

    xml_file = sys.argv[1]
    print(f"Parsing file: {xml_file}")
    cards = parse_xml(xml_file)
    insert_cards(cards)
