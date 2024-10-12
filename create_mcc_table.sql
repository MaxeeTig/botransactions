CREATE TABLE mcc (
    mcc INT PRIMARY KEY,
    edited_description VARCHAR(255),
    combined_description VARCHAR(255),
    usda_description VARCHAR(255),
    irs_description VARCHAR(255),
    irs_reportable ENUM('Yes', 'No')
);
