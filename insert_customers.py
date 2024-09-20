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
    namespace = {'ns': 'http://sv.bpc.in/SVXP/Customers'}
    customers = []

    for customer in root.findall('ns:customer', namespace):
        customer_data = {
            'customer_id': customer.get('customer_id'),
            'inst_id': customer.find('ns:inst_id', namespace).text,
            'customer_number': customer.find('ns:customer_number', namespace).text,
            'customer_relation': customer.find('ns:customer_relation', namespace).text if customer.find('ns:customer_relation', namespace) is not None else None,
            'status': customer.find('ns:status', namespace).text,
            'contract': {
                'contract_id': customer.find('ns:contract', namespace).get('contract_id'),
                'contract_number': customer.find('ns:contract/ns:contract_number', namespace).text,
                'agent_id': customer.find('ns:contract/ns:agent_id', namespace).text,
                'agent_number': customer.find('ns:contract/ns:agent_number', namespace).text,
                'contract_type': customer.find('ns:contract/ns:contract_type', namespace).text,
                'product_id': customer.find('ns:contract/ns:product_id', namespace).text,
                'product_number': customer.find('ns:contract/ns:product_number', namespace).text,
                'start_date': customer.find('ns:contract/ns:start_date', namespace).text
            },
            'person': {
                'person_id': customer.find('ns:person', namespace).get('person_id') if customer.find('ns:person', namespace) is not None else None,
                'surname': customer.find('ns:person/ns:person_name/ns:surname', namespace).text if customer.find('ns:person/ns:person_name/ns:surname', namespace) is not None else None,
                'first_name': customer.find('ns:person/ns:person_name/ns:first_name', namespace).text if customer.find('ns:person/ns:person_name/ns:first_name', namespace) is not None else None,
                'identity_card': {
                    'id_type': customer.find('ns:person/ns:identity_card/ns:id_type', namespace).text if customer.find('ns:person/ns:identity_card/ns:id_type', namespace) is not None else None,
                    'id_series': customer.find('ns:person/ns:identity_card/ns:id_series', namespace).text if customer.find('ns:person/ns:identity_card/ns:id_series', namespace) is not None else None,
                    'id_number': customer.find('ns:person/ns:identity_card/ns:id_number', namespace).text if customer.find('ns:person/ns:identity_card/ns:id_number', namespace) is not None else None
                }
            } if customer.find('ns:person', namespace) is not None else None,
            'address': {
                'address_id': customer.find('ns:address', namespace).get('address_id') if customer.find('ns:address', namespace) is not None else None,
                'address_type': customer.find('ns:address/ns:address_type', namespace).text if customer.find('ns:address/ns:address_type', namespace) is not None else None,
                'country': customer.find('ns:address/ns:country', namespace).text if customer.find('ns:address/ns:country', namespace) is not None else None,
                'region': customer.find('ns:address/ns:address_name/ns:region', namespace).text if customer.find('ns:address/ns:address_name/ns:region', namespace) is not None else None,
                'city': customer.find('ns:address/ns:address_name/ns:city', namespace).text if customer.find('ns:address/ns:address_name/ns:city', namespace) is not None else None,
                'street': customer.find('ns:address/ns:address_name/ns:street', namespace).text if customer.find('ns:address/ns:address_name/ns:street', namespace) is not None else None,
                'house': customer.find('ns:address/ns:house', namespace).text if customer.find('ns:address/ns:house', namespace) is not None else None
            } if customer.find('ns:address', namespace) is not None else None,
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
        print ("Connect to DB successfull!")

        cursor = conn.cursor()

        for customer in customers:
            # Insert customer data
            insert_customer_query = """
            INSERT INTO customers (customer_id, inst_id, customer_number, customer_relation, status)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_customer_query, (
                customer['customer_id'],
                customer['inst_id'],
                customer['customer_number'],
                customer['customer_relation'],
                customer['status']
            ))

            # Insert contract data
            insert_contract_query = """
            INSERT INTO contracts (contract_id, customer_id, contract_number, agent_id, agent_number, contract_type, product_id, product_number, start_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_contract_query, (
                customer['contract']['contract_id'],
                customer['customer_id'],
                customer['contract']['contract_number'],
                customer['contract']['agent_id'],
                customer['contract']['agent_number'],
                customer['contract']['contract_type'],
                customer['contract']['product_id'],
                customer['contract']['product_number'],
                customer['contract']['start_date']
            ))

            # Insert person data
            insert_person_query = """
            INSERT INTO persons (person_id, customer_id, surname, first_name, id_type, id_series, id_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            if customer['person'] is not None:
                cursor.execute(insert_person_query, (
                    customer['person']['person_id'],
                    customer['customer_id'],
                    customer['person']['surname'],
                    customer['person']['first_name'],
                    customer['person']['identity_card']['id_type'],
                    customer['person']['identity_card']['id_series'],
                    customer['person']['identity_card']['id_number']
                ))

            # Insert address data
            insert_address_query = """
            INSERT INTO addresses (address_id, customer_id, address_type, country, region, city, street, house)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            if customer['address'] is not None:
                cursor.execute(insert_address_query, (
                    customer['address']['address_id'],
                    customer['customer_id'],
                    customer['address']['address_type'],
                    customer['address']['country'],
                    customer['address']['region'],
                    customer['address']['city'],
                    customer['address']['street'],
                    customer['address']['house']
                ))

        conn.commit()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    customers = parse_xml('customers_prod.xml')
    insert_customers(customers)
