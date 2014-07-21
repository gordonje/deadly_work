UPDATE states_naics_3
SET expect_fatals_sum = the_sum
FROM (
	SELECT
		  state_code
		, SUM(expect_fatals) as the_sum
	FROM states_industries
	-- exclude agri industries
	WHERE industry_code NOT LIKE '1%'
	-- narrow to 3-digit NAICS
	AND CHAR_LENGTH(industry_code) = 3
	GROUP BY 
		  state_code
) as stind
WHERE states_naics_3.state_code = stind.state_code;