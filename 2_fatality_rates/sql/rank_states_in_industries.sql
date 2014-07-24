UPDATE states_industries
SET state_rank = the_rank 
FROM (
	SELECT 
		  state_code
		, industry_code
		, fatals_per_100k
		, rank() OVER (PARTITION BY industry_code ORDER BY fatals_per_100k DESC) as the_rank
	FROM states_industries
	WHERE years_count >= 5
	AND fatals_sum IS NOT NULL
) as a
WHERE a.state_code = states_industries.state_code
	AND a.industry_code = states_industries.industry_code;