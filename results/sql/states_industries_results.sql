SELECT
	  states_industries.state_code
	, areas.cfoi_name as state
	, states_industries.industry_code
	, industries.cfoi_name as industry
	, states_industries.emplvl_sum
	, states_industries.fatals_sum
	, states_industries.expect_fatals
	, states_industries.fatals_per_100k
	, states_industries.state_rank
FROM states_industries
JOIN areas
  ON states_industries.state_code = LEFT(areas.cew_code, 2)
JOIN industries
  ON states_industries.industry_code = industries.cew_code
ORDER BY 
	  states_industries.industry_code
	, states_industries.fatals_per_100k DESC;