UPDATE states_naics_3
SET oe_industries_count = the_count
FROM (
	SELECT 
		  state_code
		, COUNT(*) as the_count
	FROM states_industries
	WHERE expect_fatals > 0
	GROUP BY 
		  state_code	
) stind
WHERE states_naics_3.state_code = stind.state_code;