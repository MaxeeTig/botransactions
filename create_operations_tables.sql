CREATE TABLE operations (
    oper_id VARCHAR(255) PRIMARY KEY,
    oper_type VARCHAR(255),
    msg_type VARCHAR(255),
    sttl_type VARCHAR(255),
    status VARCHAR(255),
    oper_date DATETIME,
    host_date DATETIME,
    amount_value DECIMAL(19, 4),
    currency VARCHAR(3),
    originator_refnum VARCHAR(255),
    is_reversal BOOLEAN,
    merchant_number VARCHAR(255),
    mcc VARCHAR(255),
    merchant_name VARCHAR(255),
    merchant_street VARCHAR(255),
    merchant_city VARCHAR(255),
    merchant_region VARCHAR(255),
    merchant_country VARCHAR(255),
    merchant_postcode VARCHAR(255),
    terminal_type VARCHAR(255),
    terminal_number VARCHAR(255)
);

CREATE TABLE issuers (
    oper_id VARCHAR(255),
    inst_id VARCHAR(255),
    network_id VARCHAR(255),
    card_id VARCHAR(255),
    card_instance_id VARCHAR(255),
    card_seq_number VARCHAR(255),
    card_expir_date DATE,
    card_country VARCHAR(255),
    card_network_id VARCHAR(255),
    auth_code VARCHAR(255),
    FOREIGN KEY (oper_id) REFERENCES operations(oper_id)
);

CREATE TABLE acquirers (
    oper_id VARCHAR(255),
    inst_id VARCHAR(255),
    network_id VARCHAR(255),
    merchant_id VARCHAR(255),
    terminal_id VARCHAR(255),
    FOREIGN KEY (oper_id) REFERENCES operations(oper_id)
);

CREATE TABLE transactions (
    transaction_id VARCHAR(255) PRIMARY KEY,
    oper_id VARCHAR(255),
    transaction_type VARCHAR(255),
    posting_date DATETIME,
    debit_entry_id VARCHAR(255),
    debit_account_number VARCHAR(255),
    debit_currency VARCHAR(3),
    debit_amount_value DECIMAL(19, 4),
    debit_amount_currency VARCHAR(3),
    credit_entry_id VARCHAR(255),
    credit_account_number VARCHAR(255),
    credit_currency VARCHAR(3),
    credit_amount_value DECIMAL(19, 4),
    credit_amount_currency VARCHAR(3),
    amount_purpose VARCHAR(255),
    FOREIGN KEY (oper_id) REFERENCES operations(oper_id)
);
