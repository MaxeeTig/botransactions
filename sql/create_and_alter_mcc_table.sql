use botransactions;
CREATE TABLE mcc (
    mcc INT PRIMARY KEY,
    edited_description VARCHAR(255),
    combined_description VARCHAR(255),
    usda_description VARCHAR(255),
    irs_description VARCHAR(255),
    irs_reportable ENUM('Yes', 'No')
);

USE botransactions;

ALTER TABLE mcc
    MODIFY COLUMN mcc INT COMMENT 'Merchant Category Code',
    MODIFY COLUMN edited_description VARCHAR(255) COMMENT 'Edited description of the MCC',
    MODIFY COLUMN combined_description VARCHAR(255) COMMENT 'Combined description of the MCC',
    MODIFY COLUMN usda_description VARCHAR(255) COMMENT 'USDA description of the MCC',
    MODIFY COLUMN irs_description VARCHAR(255) COMMENT 'IRS description of the MCC',
    MODIFY COLUMN irs_reportable ENUM('Yes', 'No') COMMENT 'Indicates if the MCC is reportable to the IRS';

ALTER TABLE mcc COMMENT = 'Table storing Merchant Category Codes (MCC) with various descriptions and reportable status';
