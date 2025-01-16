use botransactions;
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

ALTER TABLE cards
    MODIFY COLUMN card_id VARCHAR(255) PRIMARY KEY COMMENT 'Unique identifier for the card',
    MODIFY COLUMN inst_id VARCHAR(255) NOT NULL COMMENT 'Institution identifier for card',
    MODIFY COLUMN card_number VARCHAR(255) NOT NULL COMMENT 'Full card number',
    MODIFY COLUMN card_mask VARCHAR(255) NOT NULL COMMENT 'Masked card number for display purposes',
    MODIFY COLUMN card_type VARCHAR(255) NOT NULL COMMENT 'Type of the card (e.g., credit, debit, gold, standard)',
    MODIFY COLUMN country VARCHAR(255) NOT NULL COMMENT 'Country where the card is issued',
    MODIFY COLUMN category VARCHAR(255) NOT NULL COMMENT 'Category of the card',
    MODIFY COLUMN reg_date DATE NOT NULL COMMENT 'Registration date of the card',
    MODIFY COLUMN customer_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the customer',
    MODIFY COLUMN contract_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the contract associated with the card';

ALTER TABLE cards COMMENT = 'Table storing details of cards issued to customers';



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

ALTER TABLE cardholders
    MODIFY COLUMN cardholder_id VARCHAR(255) PRIMARY KEY COMMENT 'Unique identifier for the cardholder',
    MODIFY COLUMN card_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the card associated with the cardholder',
    MODIFY COLUMN cardholder_number VARCHAR(255) NOT NULL COMMENT 'Cardholder number',
    MODIFY COLUMN cardholder_name VARCHAR(255) NOT NULL COMMENT 'Name of the cardholder',
    MODIFY COLUMN person_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the person associated with the cardholder',
    MODIFY COLUMN address_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the address associated with the cardholder',
    ADD CONSTRAINT fk_card FOREIGN KEY (card_id) REFERENCES cards(card_id),
    ADD CONSTRAINT fk_person FOREIGN KEY (person_id) REFERENCES persons(person_id),
    ADD CONSTRAINT fk_address FOREIGN KEY (address_id) REFERENCES addresses(address_id);

ALTER TABLE cardholders COMMENT = 'Table storing details of cardholders - the person in whose name the card is issued, which can be different from the customer';


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

