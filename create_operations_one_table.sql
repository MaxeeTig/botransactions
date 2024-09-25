CREATE TABLE operations (
     id INT AUTO_INCREMENT PRIMARY KEY,
     acq_inst_bin VARCHAR(10),
     acquirer_account_number VARCHAR(20),
     acquirer_inst_id VARCHAR(10),
     acquirer_merchant_id VARCHAR(15),
     acquirer_network_id VARCHAR(16),
     acquirer_terminal_id VARCHAR(16),
     auth_data_account_cnvt_rate VARCHAR(12),
     auth_data_acq_device_proc_result VARCHAR(10),
     auth_data_acq_resp_code VARCHAR(8),
     auth_data_addl_data VARCHAR(25),
     auth_data_amounts VARCHAR(400),
     auth_data_atc VARCHAR(25),
     auth_data_auth_tag VARCHAR(25),
     auth_data_auth_transaction_id VARCHAR(25),
     auth_data_bin_amount VARCHAR(25),
     auth_data_bin_cnvt_rate VARCHAR(25),
     auth_data_bin_currency VARCHAR(3),
     auth_data_card_capture_cap VARCHAR(25),
     auth_data_card_data_input_cap VARCHAR(25),
     auth_data_card_data_input_mode VARCHAR(25),
     auth_data_card_data_output_cap VARCHAR(25),
     auth_data_card_presence VARCHAR(25),
     auth_data_cat_level VARCHAR(25),
     auth_data_certificate_method VARCHAR(25),
     auth_data_crdh_auth_cap VARCHAR(25),
     auth_data_crdh_auth_entity VARCHAR(25),
     auth_data_crdh_auth_method VARCHAR(25),
     auth_data_crdh_presence VARCHAR(25),
     auth_data_cvr VARCHAR(25),
     auth_data_cvv2_presence VARCHAR(25),
     auth_data_cvv2_result VARCHAR(25),
     auth_data_device_date DATETIME ,
     auth_data_emv_data VARCHAR(255),
     auth_data_external_auth_id VARCHAR(20),
     auth_data_external_orig_id VARCHAR(20),
     auth_data_is_advice VARCHAR(1),
     auth_data_is_completed VARCHAR(1),
     auth_data_is_early_emv VARCHAR(1),
     auth_data_is_repeat VARCHAR(1),
     auth_data_network_amount VARCHAR(25),
     auth_data_network_cnvt_date DATETIME,
     auth_data_network_currency VARCHAR(3),
     auth_data_pin_capture_cap VARCHAR(25),
     auth_data_pin_presence VARCHAR(25),
     auth_data_pos_cond_code VARCHAR(25),
     auth_data_pos_entry_mode VARCHAR(25),
     auth_data_proc_mode VARCHAR(25),
     auth_data_proc_type VARCHAR(25),
     auth_data_resp_code VARCHAR(25),
     auth_data_service_code VARCHAR(25),
     auth_data_terminal_operating_env VARCHAR(25),
     auth_data_terminal_output_cap VARCHAR(25),
     auth_data_trace_number VARCHAR(25),
     auth_data_tvr VARCHAR(25),
     auth_data_ucaf_indicator VARCHAR(10),
     host_date DATETIME,
     is_reversal VARCHAR(1),
     issuer_auth_code VARCHAR(10),
     issuer_card_country VARCHAR(25),
     issuer_card_expir_date VARCHAR(25),
     issuer_card_id VARCHAR(25),
     issuer_card_instance_id VARCHAR(25),
     issuer_card_network_id VARCHAR(25),
     issuer_card_number VARCHAR(19),
     issuer_card_seq_number VARCHAR(10),
     issuer_inst_id VARCHAR(10),
     issuer_network_id VARCHAR(25),
     mcc VARCHAR(4),
     merchant_city VARCHAR(50),
     merchant_country VARCHAR(50),
     merchant_name VARCHAR(50),
     merchant_number VARCHAR(15),
     merchant_postcode VARCHAR(10),
     merchant_region VARCHAR(50),
     merchant_street VARCHAR(50),
     msg_type VARCHAR(8),
     network_refnum VARCHAR(50),
     oper_amount_amount_value VARCHAR(25),
     oper_amount_currency VARCHAR(3),
     oper_date DATETIME,
     oper_id VARCHAR(20),
     oper_surcharge_amount_amount_value VARCHAR(25),
     oper_surcharge_amount_currency VARCHAR(3),
     oper_type VARCHAR(8),
     original_id VARCHAR(50),
     originator_refnum VARCHAR(25),
     payment_order_id VARCHAR(25),
     status VARCHAR(8),
     sttl_amount_amount_value VARCHAR(25),
     sttl_amount_currency VARCHAR(3),
     sttl_type VARCHAR(8),
     terminal_number VARCHAR(15),
     terminal_type VARCHAR(8),
     transaction_amount_purpose VARCHAR(25),
     transaction_conversion_rate VARCHAR(25),
     transaction_credit_entry VARCHAR(25),
     transaction_debit_entry VARCHAR(25),
     transaction_fee VARCHAR(25),
     transaction_posting_date DATETIME,
     transaction_transaction_id VARCHAR(50),
     transaction_transaction_type VARCHAR(50)
 );