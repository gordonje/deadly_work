CREATE TABLE IF NOT EXISTS osha.inspections (
				  activity_nr int8
				, reporting_id int8
				, state_flag VARCHAR(2)
				, estab_name VARCHAR(100)
				, site_address VARCHAR(255)
				, site_city VARCHAR(255)
				, site_state VARCHAR(255)
				, site_zip VARCHAR(10)
				, owner_type VARCHAR(255)
				, owner_code VARCHAR(255)
				, adv_notice VARCHAR(255)
				, safety_hlth VARCHAR(255)
				, sic_code VARCHAR(255)
				, naics_code VARCHAR(255)
				, insp_type VARCHAR(255)
				, insp_scope VARCHAR(255)
				, why_no_insp VARCHAR(10)
				, union_status VARCHAR(255)
				, safety_manuf VARCHAR(255)
				, safety_const VARCHAR(255)
				, safety_marit VARCHAR(255)
				, health_manuf VARCHAR(255)
				, health_const VARCHAR(255)
				, health_marit VARCHAR(255)
				, migrant VARCHAR(255)
				, mail_street VARCHAR(255)
				, mail_city VARCHAR(255)
				, mail_state VARCHAR(255)
				, mail_zip VARCHAR(255)
				, host_est_key VARCHAR(255)
				, nr_in_estab VARCHAR(10)
				, open_date DATE
				, case_mod_date DATE
				, close_conf_date DATE
				, close_case_date DATE
				, open_year int4
				, case_mod_year int4
				, close_conf_year int4
				, close_case_year int4
				, osha_accident_indicator VARCHAR(255)
				, violation_type_s VARCHAR(5)
				, violation_type_o VARCHAR(5)
				, violation_type_r VARCHAR(5)
				, violation_type_u VARCHAR(5)
				, violation_type_w VARCHAR(5)
				, inspection_to_filter VARCHAR(255)
				);

-- insp_type	Alphanumeric, Length:1
-- insp_scope	Alphanumeric, Length:1
-- why_no_insp	Alphanumeric, Length:1
-- owner_type	Alphanumeric, Length:1
-- site_city	Alphanumeric, Length:30

-- estab_name	Alphanumeric, Length:50
-- health_const	Alphanumeric, Length:1
-- health_manuf	Alphanumeric, Length:1
-- health_marit	Alphanumeric, Length:1
-- union_status	Alphanumeric, Length:1
-- host_est_key	Alphanumeric, Length:17
-- ld_dt	date
-- mail_city	Alphanumeric, Length:30
-- mail_zip	Numeric, Length:5
-- mail_state	Alphanumeric, Length:2
-- mail_street	Alphanumeric, Length:50
-- migrant	Alphanumeric, Length:1
-- nr_in_estab	Numeric, Length:5

-- safety_const	Alphanumeric, Length:1
-- safety_manuf	Alphanumeric, Length:1
-- safety_marit	Alphanumeric, Length:1
-- safety_hlth	Alphanumeric, Length:1
-- sic_code	Numeric, Length:4
-- site_state	Alphanumeric, Length:2
-- site_address	Alphanumeric, Length:50
-- state_flag	Alphanumeric, Length:1
-- naics_code	Numeric, Length:6
-- zip_dim_id	int4
-- indstry_dim_id	int4
-- owner_code	Numeric, Length:4
-- adv_notice	Alphanumeric, Length:1
-- open_date	Numeric, Length=8