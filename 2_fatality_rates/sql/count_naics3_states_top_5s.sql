-- In how many industries does each state have one of the worst five fatality rates?
UPDATE states_naics_3
SET top_5_count = the_count
FROM (
	SELECT
		  state_code
		, COUNT(*) as the_count
	FROM states_industries a
	WHERE state_rank <= 5
		AND industry_code NOT IN (
			SELECT cew_code
			FROM industries
			WHERE fatals_sum = 0
	) -- industries without deaths (excludes 241 industries, or 19 percent) -- check count
		AND industry_code NOT IN (
			SELECT industry_code
			FROM states_industries
			GROUP BY industry_code
			HAVING COUNT(*) <= 5
	) -- industries that are in fewer than five states (none) -- check count
		AND industry_code NOT IN (
			SELECT industry_code
			FROM states_industries
			WHERE fatals_sum > 0
			GROUP BY industry_code
			HAVING COUNT(*) <= 5
	) -- industries with deaths in fewer than five states (675 industries, or 53 percent) -- check count
	-- and exclude agri
		AND industry_code NOT LIKE '1%'
	-- and narrow to 3-digit NAICS
		AND CHAR_LENGTH(industry_code) = 3
	GROUP BY state_code
) as a
WHERE states_naics_3.state_code = a.state_code;