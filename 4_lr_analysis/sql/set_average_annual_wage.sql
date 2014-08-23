UPDATE states_industries
SET wage_avg = the_avg
FROM (
	SELECT 
		  industry_code
		, state_code
		, AVG(avg_annual_pay) as the_avg
	FROM states_industries_years
	GROUP BY
		  industry_code
		, state_code
) as styr
WHERE
	styr.state_code = states_industries.state_code
AND styr.industry_code = states_industries.industry_code;