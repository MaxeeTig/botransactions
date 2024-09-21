CREATE TABLE cards (
    card_id VARCHAR(255) PRIMARY KEY,
    inst_id VARCHAR(255) NOT NULL,
    card_number VARCHAR(255) NOT NULL,
    card_mask VARCHAR(255) NOT NULL,
    card_type VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    reg_date DATE NOT NULL,
    customer_id VARCHAR(255) NOT NULL,
    contract_id VARCHAR(255) NOT NULL
);

CREATE TABLE cardholders (
    cardholder_id VARCHAR(255) PRIMARY KEY,
    card_id VARCHAR(255) NOT NULL,
    cardholder_number VARCHAR(255) NOT NULL,
    cardholder_name VARCHAR(255) NOT NULL,
    person_id VARCHAR(255) NOT NULL,
    address_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards(card_id),
    FOREIGN KEY (person_id) REFERENCES persons(person_id),
    FOREIGN KEY (address_id) REFERENCES addresses(address_id)
);

CREATE TABLE persons (
    person_id VARCHAR(255) PRIMARY KEY,
    surname VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    id_type VARCHAR(255) NOT NULL,
    id_series VARCHAR(255) NOT NULL,
    id_number VARCHAR(255) NOT NULL
);

CREATE TABLE addresses (
    address_id VARCHAR(255) PRIMARY KEY,
    address_type VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    street VARCHAR(255) NOT NULL,
    house VARCHAR(255) NOT NULL,
    apartment VARCHAR(255),
    postal_code VARCHAR(255)
);

CREATE TABLE card_instances (
    instance_id VARCHAR(255) PRIMARY KEY,
    card_id VARCHAR(255) NOT NULL,
    inst_id VARCHAR(255) NOT NULL,
    agent_id VARCHAR(255) NOT NULL,
    agent_number VARCHAR(255) NOT NULL,
    sequential_number VARCHAR(255) NOT NULL,
    card_status VARCHAR(255) NOT NULL,
    card_state VARCHAR(255) NOT NULL,
    iss_date DATE NOT NULL,
    start_date DATE NOT NULL,
    expiration_date DATE NOT NULL,
    pin_update_flag VARCHAR(255) NOT NULL,
    pin_request VARCHAR(255) NOT NULL,
    perso_priority VARCHAR(255) NOT NULL,
    embossing_request VARCHAR(255) NOT NULL,
    pin_mailer_request VARCHAR(255) NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards(card_id)
);

CREATE TABLE accounts (
    account_id VARCHAR(255) PRIMARY KEY,
    card_id VARCHAR(255) NOT NULL,
    account_number VARCHAR(255) NOT NULL,
    account_type VARCHAR(255) NOT NULL,
    currency VARCHAR(255) NOT NULL,
    account_status VARCHAR(255) NOT NULL,
    link_flag VARCHAR(255) NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards(card_id)
);

CREATE TABLE flexible_data (
    entity_type VARCHAR(255) NOT NULL,
    field_name VARCHAR(255) NOT NULL,
    field_value VARCHAR(255) NOT NULL
);
