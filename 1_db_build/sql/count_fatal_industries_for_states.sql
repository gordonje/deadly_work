UPDATE areas
SET fatal_industries_count = the_count
FROM (
	SELECT
		  state_code
		, COUNT(*) as the_count
	FROM (
	-- we have to go down to the state-industry-year level
	-- because we haven't yet excluded states/industries where no fatals were reported
		SELECT
			  state_code
			, industry_code
			, SUM(emplvl)
			, SUM(fatals)
		FROM states_industries_years
		GROUP BY
			  state_code
			, industry_code
		HAVING SUM(emplvl) > 0
		AND SUM(fatals) > 0
	) as siy
	GROUP BY state_code
) as stind
WHERE stind.state_code = LEFT(areas.cew_code, 2);