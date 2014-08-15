UPDATE industries
SET sort_order = the_rank 
FROM (
	SELECT 
		  industry_code
		, rank() OVER (ORDER BY residual) as the_rank
	FROM states_industries
	JOIN industries
	ON industry_code = cew_code
	WHERE state_code = '48'
	AND display_level = 3
	AND industry_code not like '1%'
	AND residual is not NULL
	ORDER BY states_industries.residual DESC
) as a
WHERE a.industry_code = cew_code;