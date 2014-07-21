UPDATE states_naics_3
SET oe_industries_count = the_count
FROM (
	SELECT 
		  state_code
		, COUNT(*) as the_count
	FROM states_industries
	WHERE residual > 0
	  AND CHAR_LENGTH(industry_code) = 3
	GROUP BY 
		  state_code	
) stind
WHERE states_naics_3.state_code = stind.state_code;