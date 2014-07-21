CREATE TABLE states_naics_3
AS 
SELECT
	  LEFT(areas.cew_code, 2) as state_code
	, CASE
			WHEN areas.cew_code = '11000' THEN areas.cew_name
			ELSE TRIM(LEFT(areas.cew_name, POSITION(' -' in areas.cew_name)))
		END as state_name
	, areas.abbrv
	, stind.fatals_sum
	-- should this be the sum of employment levels across all years or just years where fatalities are reported?
	, stind.emplvl_sum
	, (stind.fatals_sum / stind.emplvl_sum) * 100000 as fatals_per_100k_unadj
FROM areas
JOIN (
	SELECT 
		  state_code
		, SUM(fatals_sum) as fatals_sum
	-- same question?
		, SUM(emplvl_sum) as emplvl_sum
	FROM states_industries
	-- exclude agri industries
	WHERE industry_code NOT LIKE '1%'
	-- narrow to 3-digit NAICS
	AND CHAR_LENGTH(industry_code) = 3
	GROUP BY state_code
) as stind
ON LEFT(areas.cew_code, 2) = stind.state_code