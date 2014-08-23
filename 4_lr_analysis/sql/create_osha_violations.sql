CREATE TABLE osha.violations (
	  activity_nr numeric
	, citation_id varchar(7)
	, delete_flag varchar(1)
	, standard varchar(22)
	, viol_type varchar(1)
	, issuance_date date
	, abate_date varchar(10)
	, abate_complete varchar(1)
	, current_penalty numeric
	, initial_penalty numeric
	, contest_date date
	, final_order_date date
	, nr_instances numeric
	, nr_exposed numeric
	, rec varchar(1)
	, gravity varchar(2)
	, emphasis varchar(1)
	, hazcat varchar(10)
	, fta_insp_nr numeric
	, fta_issuance_date date
	, fta_penalty varchar(10)
	, fta_contest_date date
	, fta_final_order_date date
	, hazsub1 varchar(4)
	, hazsub2 varchar(4)
	, hazsub3 varchar(4)
	, hazsub4 varchar(4)
	, hazsub5 varchar(4)
);