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
