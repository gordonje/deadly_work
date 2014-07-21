UPDATE industries
SET fatal_states_count = the_count
FROM (
	SELECT
		  industry_code
		, COUNT(*) as the_count
	FROM (
	-- we have to go down to the state-industry-year level
	-- because we haven't yet excluded states/industries where no fatals were reported
		SELECT
			  industry_code
			, state_code
			, SUM(emplvl)
			, SUM(fatals)
		FROM states_industries_years
		GROUP BY
			  industry_code
			, state_code
		HAVING SUM(emplvl) > 0
		AND SUM(fatals) > 0
	) as siy
	GROUP BY industry_code
) as stind
WHERE stind.industry_code = industries.cew_code;