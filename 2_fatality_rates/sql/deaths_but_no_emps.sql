SELECT 
	  LEFT(areas.cew_code, 2) as state_code
	, areas.cfoi_name as state
	, industries.cew_code as industry_code
	, industries.cfoi_name as industry
	, siy.year
	, siy.fatals
	, siy.emplvl
FROM states_industries_years siy
JOIN areas
  ON siy.state_code = LEFT(areas.cew_code, 2)
JOIN industries
  ON siy.industry_code = industries.cew_code
WHERE siy.fatals IS NOT NULL
  AND siy.emplvl = 0
ORDER BY 
	  areas.cfoi_name
	, industries.cew_code
	, siy.year;