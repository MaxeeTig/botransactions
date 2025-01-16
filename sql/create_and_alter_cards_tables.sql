use botransactions;

CREATE TABLE IF NOT EXISTS cards (
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
    MODIFY COLUMN card_id VARCHAR(255) COMMENT 'Unique identifier for the card',
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

CREATE TABLE IF NOT EXISTS persons (
    person_id VARCHAR(255) PRIMARY KEY,
    surname VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    id_type VARCHAR(255) NOT NULL,
    id_series VARCHAR(255) NOT NULL,
    id_number VARCHAR(255) NOT NULL,
    customer_id VARCHAR(255) NOT NULL
);

ALTER TABLE persons
    MODIFY COLUMN person_id VARCHAR(255) COMMENT 'Unique identifier for the person',
    MODIFY COLUMN surname VARCHAR(255) NOT NULL COMMENT 'Surname of the person',
    MODIFY COLUMN first_name VARCHAR(255) NOT NULL COMMENT 'First name of the person',
    MODIFY COLUMN id_type VARCHAR(255) NOT NULL COMMENT 'Type of identification document',
    MODIFY COLUMN id_series VARCHAR(255) NOT NULL COMMENT 'Series of the identification document',
    MODIFY COLUMN id_number VARCHAR(255) NOT NULL COMMENT 'Number of the identification document',
    MODIFY COLUMN customer_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the customer';

ALTER TABLE persons COMMENT = 'Table storing details of persons associated with cards';

CREATE TABLE IF NOT EXISTS addresses (
    address_id VARCHAR(255) PRIMARY KEY,
    address_type VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    street VARCHAR(255) NOT NULL,
    house VARCHAR(255) NOT NULL,
    postal_code VARCHAR(255) NOT NULL,
    customer_id VARCHAR(255) NOT NULL
);

ALTER TABLE addresses
    MODIFY COLUMN address_id VARCHAR(255) COMMENT 'Unique identifier for the address',
    MODIFY COLUMN address_type VARCHAR(255) NOT NULL COMMENT 'Type of address (e.g., home, work)',
    MODIFY COLUMN country VARCHAR(255) NOT NULL COMMENT 'Country of the address',
    MODIFY COLUMN region VARCHAR(255) NOT NULL COMMENT 'Region of the address',
    MODIFY COLUMN city VARCHAR(255) NOT NULL COMMENT 'City of the address',
    MODIFY COLUMN street VARCHAR(255) NOT NULL COMMENT 'Street of the address',
    MODIFY COLUMN house VARCHAR(255) NOT NULL COMMENT 'House number of the address',
    MODIFY COLUMN postal_code VARCHAR(255) NOT NULL COMMENT 'Postal code of the address',
    MODIFY COLUMN customer_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the customer';

ALTER TABLE addresses COMMENT = 'Table storing details of addresses associated with cardholders';

CREATE TABLE IF NOT EXISTS cardholders (
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
    MODIFY COLUMN cardholder_id VARCHAR(255) COMMENT 'Unique identifier for the cardholder',
    MODIFY COLUMN card_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the card associated with the cardholder',
    MODIFY COLUMN cardholder_number VARCHAR(255) NOT NULL COMMENT 'Cardholder number',
    MODIFY COLUMN cardholder_name VARCHAR(255) NOT NULL COMMENT 'Name of the cardholder',
    MODIFY COLUMN person_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the person associated with the cardholder',
    MODIFY COLUMN address_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the address associated with the cardholder',
    ADD CONSTRAINT fk_card FOREIGN KEY (card_id) REFERENCES cards(card_id),
    ADD CONSTRAINT fk_person FOREIGN KEY (person_id) REFERENCES persons(person_id),
    ADD CONSTRAINT fk_address FOREIGN KEY (address_id) REFERENCES addresses(address_id);

ALTER TABLE cardholders COMMENT = 'Table storing details of cardholders - the person in whose name the card is issued, which can be different from the customer';

-- Step 1: Create the table without the foreign key constraint
CREATE TABLE IF NOT EXISTS card_instances (
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
    pin_mailer_request VARCHAR(255) NOT NULL
);

-- Step 2: Add the foreign key constraint separately
ALTER TABLE card_instances
    ADD CONSTRAINT fk_card FOREIGN KEY (card_id) REFERENCES cards(card_id);

-- Step 3: Add comments to the columns
ALTER TABLE card_instances
    MODIFY COLUMN instance_id VARCHAR(255) COMMENT 'Unique identifier for the card instance',
    MODIFY COLUMN card_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the card associated with the instance',
    MODIFY COLUMN inst_id VARCHAR(255) NOT NULL COMMENT 'Institution identifier for the card instance',
    MODIFY COLUMN agent_id VARCHAR(255) NOT NULL COMMENT 'Agent identifier for the card instance',
    MODIFY COLUMN agent_number VARCHAR(255) NOT NULL COMMENT 'Agent number for the card instance',
    MODIFY COLUMN sequential_number VARCHAR(255) NOT NULL COMMENT 'Sequential number for the card instance',
    MODIFY COLUMN card_status VARCHAR(255) NOT NULL COMMENT 'Status of the card instance',
    MODIFY COLUMN card_state VARCHAR(255) NOT NULL COMMENT 'State of the card instance',
    MODIFY COLUMN iss_date DATE NOT NULL COMMENT 'Issue date of the card instance',
    MODIFY COLUMN start_date DATE NOT NULL COMMENT 'Start date of the card instance',
    MODIFY COLUMN expiration_date DATE NOT NULL COMMENT 'Expiration date of the card instance',
    MODIFY COLUMN pin_update_flag VARCHAR(255) NOT NULL COMMENT 'PIN update flag for the card instance',
    MODIFY COLUMN pin_request VARCHAR(255) NOT NULL COMMENT 'PIN request for the card instance',
    MODIFY COLUMN perso_priority VARCHAR(255) NOT NULL COMMENT 'Personalization priority for the card instance',
    MODIFY COLUMN embossing_request VARCHAR(255) NOT NULL COMMENT 'Embossing request for the card instance',
    MODIFY COLUMN pin_mailer_request VARCHAR(255) NOT NULL COMMENT 'PIN mailer request for the card instance';

-- Step 4: Add a comment to the table
ALTER TABLE card_instances COMMENT = 'Table storing details of card instances';





-- Step 1: Create the table without the foreign key constraint
CREATE TABLE IF NOT EXISTS accounts (
    account_id VARCHAR(255) PRIMARY KEY,
    card_id VARCHAR(255) NOT NULL,
    account_number VARCHAR(255) NOT NULL,
    account_type VARCHAR(255) NOT NULL,
    currency VARCHAR(255) NOT NULL,
    account_status VARCHAR(255) NOT NULL,
    link_flag VARCHAR(255) NOT NULL
);

-- Step 2: Add the foreign key constraint separately
ALTER TABLE accounts
    ADD CONSTRAINT fk_card FOREIGN KEY (card_id) REFERENCES cards(card_id);

-- Step 3: Add comments to the columns
ALTER TABLE accounts
    MODIFY COLUMN account_id VARCHAR(255) COMMENT 'Unique identifier for the account',
    MODIFY COLUMN card_id VARCHAR(255) NOT NULL COMMENT 'Unique identifier for the card associated with the account',
    MODIFY COLUMN account_number VARCHAR(255) NOT NULL COMMENT 'Account number',
    MODIFY COLUMN account_type VARCHAR(255) NOT NULL COMMENT 'Type of the account',
    MODIFY COLUMN currency VARCHAR(255) NOT NULL COMMENT 'Currency of the account',
    MODIFY COLUMN account_status VARCHAR(255) NOT NULL COMMENT 'Status of the account',
    MODIFY COLUMN link_flag VARCHAR(255) NOT NULL COMMENT 'Link flag for the account';

-- Step 4: Add a comment to the table
ALTER TABLE accounts COMMENT = 'Table storing details of accounts associated with cards';

