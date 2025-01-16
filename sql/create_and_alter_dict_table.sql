use botransactions;
CREATE TABLE dict_table (
    id INT PRIMARY KEY,
    dict VARCHAR(10),
    code VARCHAR(10),
    dkey VARCHAR(15),
    text_e VARCHAR(2048),
    entity_type VARCHAR(10),
    is_numeric BOOLEAN,
    is_editable BOOLEAN,
    inst_id INT,
    module_code VARCHAR(10)
);

USE botransactions;

ALTER TABLE dict_table
    MODIFY COLUMN id INT COMMENT 'Unique identifier for the dictionary entry',
    MODIFY COLUMN dict VARCHAR(10) COMMENT 'Dictionary identifier, specifying type of dictionary, e.g. OPTP - operation types, OPST - operation statuses',
    MODIFY COLUMN code VARCHAR(10) COMMENT 'Code associated with the dictionary entry',
    MODIFY COLUMN dkey VARCHAR(15) COMMENT 'Value of the dictionary entry (key), e.g. OPTP0001 - ATM Cash withdrawal, OPST0100 - Ready to process',
    MODIFY COLUMN text_e VARCHAR(2048) COMMENT 'Text description in English',
    MODIFY COLUMN entity_type VARCHAR(10) COMMENT 'Type of the entity',
    MODIFY COLUMN is_numeric BOOLEAN COMMENT 'Indicates if the entry is numeric',
    MODIFY COLUMN is_editable BOOLEAN COMMENT 'Indicates if the entry is editable',
    MODIFY COLUMN inst_id INT COMMENT 'Institution identifier to which entry can be applied, 9999 - all institutions',
    MODIFY COLUMN module_code VARCHAR(10) COMMENT 'Module code to which record can be applied (ACQ - acquiring, CRD - loan, ATM - automated teller machine related';

ALTER TABLE dict_table COMMENT = 'Table containing different back office dictionaries of operation types, statuses, institutions, and applicable modules';

