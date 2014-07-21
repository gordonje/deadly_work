CREATE TABLE states_naics_3
AS 
SELECT
	  LEFT(areas.cew_code, 2) as state_code
	, CASE
			WHEN areas.cew_code = '11000' THEN areas.cew_name
			ELSE TRIM(LEFT(areas.cew_name, POSITION(' -' in areas.cew_name)))
		END as state_name
	, areas.abbrv
	, areas.emplvl_total
	, si.emplvl_capd
	, si.fatals_capd
	, si.expect_fatals_sum
-- formula for residual:
-- total number of fatalities in the state (without industry filtering) minus the sum of expected fatalities
	, fatals_capd - expect_fatals_sum as residual
FROM areas
JOIN (
	SELECT
		  state_code
		, SUM(emplvl_sum) as emplvl_capd
		, SUM(fatals_sum) as fatals_capd
		, SUM(expect_fatals) as expect_fatals_sum
	FROM states_industries 
	WHERE 
		  CHAR_LENGTH(industry_code) = 3
	GROUP BY 
		  state_code
) as si
ON si.state_code = LEFT(areas.cew_code, 2)