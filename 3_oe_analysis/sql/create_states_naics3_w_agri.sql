CREATE TABLE states_naics3_w_agri
AS 
SELECT
	  LEFT(areas.cew_code, 2) as state_code
	, CASE
			WHEN areas.cew_code = '11000' THEN areas.cew_name
			ELSE TRIM(LEFT(areas.cew_name, POSITION(' -' in areas.cew_name)))
		END as state_name
	, areas.abbrv
	, areas.emplvl_total
	, areas.fatals_total
	-- , si.emplvl_capd
	-- , si.fatals_capd
	, si.expect_fatals_sum
-- formula for residual:
-- total number of fatalities in the state (without industry filtering) minus the sum of expected fatalities
	, fatals_total - expect_fatals_sum as residual
FROM areas
JOIN (
	SELECT
		  states_industries.state_code
		-- , SUM(emplvl_sum) as emplvl_capd
		-- , SUM(fatals_sum) as fatals_capd
		, SUM(states_industries.expect_fatals) as expect_fatals_sum
	FROM states_industries
	JOIN industries 
	ON
		  states_industries.industry_code = industries.cew_code
	WHERE 
	-- narrow to 3-digit NAICS industries
		  industries.display_level = 4
	GROUP BY 
		  states_industries.state_code
) as si
ON si.state_code = LEFT(areas.cew_code, 2)