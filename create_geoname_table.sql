 CREATE TABLE geoname (
    geonameid INT,
    name VARCHAR(200) CHARACTER SET utf8,
    asciiname VARCHAR(200),
    alternatenames VARCHAR(10000),
    country_code CHAR(2)
) ENGINE=InnoDB;
