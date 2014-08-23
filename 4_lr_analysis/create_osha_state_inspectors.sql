CREATE TABLE IF NOT EXISTS osha.states_inspectors (
	  state varchar(30)
	, is_public_sector_only BOOLEAN DEFAULT FALSE
);