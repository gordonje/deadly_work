-- In how many industries does each state have the worst fatality rate?
UPDATE states_naics_3
SET top_1_count = the_count
FROM (
	SELECT
		  state_code
		, COUNT(*) as the_count
	FROM states_industries a
	WHERE state_rank <= 1
		AND industry_code NOT IN (
			SELECT cew_code
			FROM industries
			WHERE fatals_sum = 0
	) -- industries without deaths (excludes 241 industries, or 19 percent) -- check count
		AND industry_code NOT IN (
			SELECT industry_code
			FROM states_industries
			GROUP BY industry_code
			HAVING COUNT(*) <= 1
	) -- industries that are in only one state (none) -- check count
		AND industry_code NOT IN (
			SELECT industry_code
			FROM states_industries
			WHERE fatals_sum > 0
			GROUP BY industry_code
			HAVING COUNT(*) <= 1
	) -- industries with deaths only one state (281 industries, or 22 percent) -- check count
	-- and exclude agri
		AND industry_code NOT LIKE '1%'
	-- and narrow to 3-digit NAICS
		AND CHAR_LENGTH(industry_code) = 3
	GROUP BY state_code
) as a
WHERE states_naics_3.state_code = a.state_code;