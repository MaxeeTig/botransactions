use botransactions;
CREATE TABLE customers (
    customer_id VARCHAR(255) PRIMARY KEY,
    inst_id VARCHAR(255) NOT NULL,
    customer_number VARCHAR(255) NOT NULL,
    customer_relation VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL
);

CREATE TABLE contracts (
    contract_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    contract_number VARCHAR(255) NOT NULL,
    agent_id VARCHAR(255) NOT NULL,
    agent_number VARCHAR(255) NOT NULL,
    contract_type VARCHAR(255) NOT NULL,
    product_id VARCHAR(255) NOT NULL,
    product_number VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE persons (
    person_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    id_type VARCHAR(255) NOT NULL,
    id_series VARCHAR(255) NOT NULL,
    id_number VARCHAR(255) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE addresses (
    address_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    address_type VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    street VARCHAR(255) NOT NULL,
    house VARCHAR(255) NOT NULL,
    postal_code VARCHAR(255),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
