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
    namespace = {'ns': 'http://sv.bpc.in/SVXP/Cards'}
    cards = []

    for card in root.findall('ns:card', namespace):
        card_data = {
            'card_id': card.get('card_id'),
            'inst_id': card.find('ns:inst_id', namespace).text if card.find('ns:inst_id', namespace) is not None else None,
            'card_number': card.find('ns:card_number', namespace).text if card.find('ns:card_number', namespace) is not None else None,
            'card_mask': card.find('ns:card_mask', namespace).text if card.find('ns:card_mask', namespace) is not None else None,
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
                        'id_type': card.find('ns:cardholder/ns:person/ns:identity_card/ns:id_type', namespace).text if card.find('ns:cardholder/ns:person/ns:identity_card/ns:id_type', namespace) is not None else None,
                        'id_series': card.find('ns:cardholder/ns:person/ns:identity_card/ns:id_series', namespace).text if card.find('ns:cardholder/ns:person/ns:identity_card/ns:id_series', namespace) is not None else None,
                        'id_number': card.find('ns:cardholder/ns:person/ns:identity_card/ns:id_number', namespace).text if card.find('ns:cardholder/ns:person', namespace) is not None else None
                    }
                },
                'address': {
                    'address_id': card.find('ns:cardholder/ns:address', namespace).get('address_id'),
                    'address_type': card.find('ns:cardholder/ns:address/ns:address_type', namespace).text,
                    'country': card.find('ns:cardholder/ns:address/ns:country', namespace).text,
                    'region': card.find('ns:cardholder/ns:address/ns:address_name/ns:region', namespace).text,
                    'city': card.find('ns:cardholder/ns:address/ns:address_name/ns:city', namespace).text,
                    'street': card.find('ns:cardholder/ns:address/ns:address_name/ns:street', namespace).text,
                    'house': card.find('ns:cardholder/ns:address/ns:house', namespace).text,
                    'apartment': card.find('ns:cardholder/ns:address/ns:apartment', namespace).text if card.find('ns:cardholder/ns:address/ns:apartment', namespace) is not None else None,
                    'postal_code': card.find('ns:cardholder/ns:address/ns:postal_code', namespace).text if card.find('ns:cardholder/ns:address/ns:postal_code', namespace) is not None else None
                }
            },
            'card_instance': {
                'instance_id': card.find('ns:card_instance', namespace).get('instance_id'),
                'inst_id': card.find('ns:card_instance/ns:inst_id', namespace).text,
                'agent_id': card.find('ns:card_instance/ns:agent_id', namespace).text,
                'agent_number': card.find('ns:card_instance/ns:agent_number', namespace).text,
                'sequential_number': card.find('ns:card_instance/ns:sequential_number', namespace).text,
                'card_status': card.find('ns:card_instance/ns:card_status', namespace).text,
                'card_state': card.find('ns:card_instance/ns:card_state', namespace).text,
                'iss_date': card.find('ns:card_instance/ns:iss_date', namespace).text if card.find('ns:card_instance/ns:iss_date', namespace) is not None else None,
                'start_date': card.find('ns:card_instance/ns:start_date', namespace).text if card.find('ns:card_instance/ns:start_date', namespace) is not None else None,
                'expiration_date': card.find('ns:card_instance/ns:expiration_date', namespace).text if card.find('ns:card_instance/ns:expiration_date', namespace) is not None else None,
                'pin_update_flag': card.find('ns:card_instance/ns:pin_update_flag', namespace).text if card.find('ns:card_instance/ns:pin_update_flag', namespace) is not None else None,
                'pin_request': card.find('ns:card_instance/ns:pin_request', namespace).text if card.find('ns:card_instance/ns:pin_request', namespace) is not None else None,
                'perso_priority': card.find('ns:card_instance/ns:perso_priority', namespace).text if card.find('ns:card_instance/ns:perso_priority', namespace) is not None else None,
                'embossing_request': card.find('ns:card_instance/ns:embossing_request', namespace).text if card.find('ns:card_instance/ns:embossing_request', namespace) is not None else None,
                'pin_mailer_request': card.find('ns:card_instance/ns:pin_mailer_request', namespace).text if card.find('ns:card_instance/ns:pin_mailer_request', namespace) is not None else None
            },
            'account': {
                'account_id': card.find('ns:account', namespace).get('account_id'),
                'account_number': card.find('ns:account/ns:account_number', namespace).text,
                'account_type': card.find('ns:account/ns:account_type', namespace).text,
                'currency': card.find('ns:account/ns:currency', namespace).text,
                'account_status': card.find('ns:account/ns:account_status', namespace).text,
                'link_flag': card.find('ns:account/ns:link_flag', namespace).text
            },
            'flexible_data': []
        }

        for flexible_data in card.findall('ns:flexible_data', namespace):
            flexible_data_item = {
                'field_name': flexible_data.find('ns:field_name', namespace).text,
                'field_value': flexible_data.find('ns:field_value', namespace).text
            }
            card_data['flexible_data'].append(flexible_data_item)

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
        print ("Connect to DB successfull!")

        cursor = conn.cursor()

        total_records = len(cards)
        for i, card in enumerate(cards, 1):
            print(f"Inserting record {i} of {total_records}")
            # Insert card data
            insert_card_query = """
            INSERT INTO cards (card_id, inst_id, card_number, card_mask, card_type, country, category, reg_date, customer_id, contract_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_card_query, (
                card['card_id'],
                card['inst_id'],
                card['card_number'],
                card['card_mask'],
                card['card_type'],
                card['country'],
                card['category'],
                card['reg_date'],
                card['customer']['customer_id'],
                card['contract']['contract_id']
            ))
            print(f"Inserted record {i} of {total_records}")

            # Check if person_id exists in persons table
            check_person_query = """
            SELECT person_id FROM persons WHERE person_id = %s
            """
            cursor.execute(check_person_query, (card['cardholder']['person']['person_id'],))
            person_exists = cursor.fetchone()

            if not person_exists:
                # Insert person data
                insert_person_query = """
                INSERT INTO persons (person_id, surname, first_name, id_type, id_series, id_number)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_person_query, (
                    card['cardholder']['person']['person_id'],
                    card['cardholder']['person']['surname'],
                    card['cardholder']['person']['first_name'],
                    card['cardholder']['person']['identity_card']['id_type'],
                    card['cardholder']['person']['identity_card']['id_series'],
                    card['cardholder']['person']['identity_card']['id_number']
                ))
                print(f"Inserted person record {i} of {total_records}")

            # Insert cardholder data
            insert_cardholder_query = """
            INSERT INTO cardholders (cardholder_id, card_id, cardholder_number, cardholder_name, person_id, address_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_cardholder_query, (
                card['cardholder']['cardholder_id'],
                card['card_id'],
                card['cardholder']['cardholder_number'],
                card['cardholder']['cardholder_name'],
                card['cardholder']['person']['person_id'],
                card['cardholder']['address']['address_id']
            ))
            print(f"Inserted cardholder record {i} of {total_records}")

            # Insert person data
            insert_person_query = """
            INSERT INTO persons (person_id, surname, first_name, id_type, id_series, id_number)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_person_query, (
                card['cardholder']['person']['person_id'],
                card['cardholder']['person']['surname'],
                card['cardholder']['person']['first_name'],
                card['cardholder']['person']['identity_card']['id_type'],
                card['cardholder']['person']['identity_card']['id_series'],
                card['cardholder']['person']['identity_card']['id_number']
            ))
            print(f"Inserted record {i} of {total_records}")

            # Insert address data
            insert_address_query = """
            INSERT INTO addresses (address_id, address_type, country, region, city, street, house, apartment, postal_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_address_query, (
                card['cardholder']['address']['address_id'],
                card['cardholder']['address']['address_type'],
                card['cardholder']['address']['country'],
                card['cardholder']['address']['region'],
                card['cardholder']['address']['city'],
                card['cardholder']['address']['street'],
                card['cardholder']['address']['house'],
                card['cardholder']['address']['apartment'],
                card['cardholder']['address']['postal_code']
            ))
            print(f"Inserted record {i} of {total_records}")

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
                card['card_instance']['sequential_number'],
                card['card_instance']['card_status'],
                card['card_instance']['card_state'],
                card['card_instance']['iss_date'],
                card['card_instance']['start_date'],
                card['card_instance']['expiration_date'],
                card['card_instance']['pin_update_flag'],
                card['card_instance']['pin_request'],
                card['card_instance']['perso_priority'],
                card['card_instance']['embossing_request'],
                card['card_instance']['pin_mailer_request']
            ))
            print(f"Inserted record {i} of {total_records}")

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
                card['account']['currency'],
                card['account']['account_status'],
                card['account']['link_flag']
            ))
            print(f"Inserted record {i} of {total_records}")

            # Insert flexible data
            for flexible_data in card['flexible_data']:
                insert_flexible_data_query = """
                INSERT INTO flexible_data (entity_type, field_name, field_value)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_flexible_data_query, (
                    'Card',
                    flexible_data['field_name'],
                    flexible_data['field_value']
                ))
                print(f"Inserted record {i} of {total_records}")

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
