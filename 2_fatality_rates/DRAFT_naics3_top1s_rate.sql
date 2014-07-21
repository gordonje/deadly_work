-- how many industries are in each state that meet our criteria?
-- and what's the rate at which each state is in the top five?
ALTER TABLE states_naics_3
ADD COLUMN top_5_ind_pool numeric,
ADD COLUMN top_5_rate numeric;

UPDATE states_naics_3
SET 
	  top_5_ind_pool = the_pool
	, top_5_rate = top_5_count / the_pool
FROM (
	SELECT
		  state_code
		, COUNT(*) as the_pool
	FROM states_industries
	WHERE industry_code NOT IN (
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