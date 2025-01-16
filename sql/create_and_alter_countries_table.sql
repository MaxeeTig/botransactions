
CREATE TABLE countries (
    id varchar(3),    
    ncode VARCHAR(3),
    sname VARCHAR(100),
    fname VARCHAR(100),
    aacode VARCHAR(2),
    aaacode VARCHAR(3)
);


ALTER TABLE countries
    CHANGE COLUMN ncode numeric_code VARCHAR(3) COMMENT 'ISO numeric code of country',
    CHANGE COLUMN sname short_name VARCHAR(100) COMMENT 'Short Cyrillic name of country',
    CHANGE COLUMN fname full_name VARCHAR(100) COMMENT 'Full Cyrillic name of country',
    MODIFY COLUMN aacode VARCHAR(2) COMMENT 'Alpha code of country 2 symbols, e.g., RU',
    MODIFY COLUMN aaacode VARCHAR(3) COMMENT 'Alpha code of country 3 symbols, e.g., RUS';

ALTER TABLE countries COMMENT = 'Table contains the list of country names and codes: alphabetic and numeric';


