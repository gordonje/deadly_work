CREATE TABLE states_naics_3
AS 
SELECT
	  LEFT(areas.cew_code, 2) as state_code
	, CASE
			WHEN areas.cew_code = '11000' THEN areas.cew_name
			ELSE TRIM(LEFT(areas.cew_name, POSITION(' -' in areas.cew_name)))
		END as state_name
	, abbrv
	, estabs_sum
	, emplvl_sum
	, fatals_sum
	, expect_fatals_sum
	, fatals_sum - expect_fatals_sum as residual
	, (fatals_sum / emplvl_sum) * 100000 as fatals_per_100k_unadj
FROM areas
JOIN (
	SELECT
		  state_code
		, SUM(estabs_sum) as estabs_sum
		, SUM(emplvl_sum) as emplvl_sum
		, SUM(fatals_sum) as fatals_sum
		, SUM(expect_fatals) as expect_fatals_sum
	FROM states_industries 
-- exclude agri
	WHERE industry_code NOT LIKE '1%'
-- and narrow to 3 digit naics codes
		AND CHAR_LENGTH(industry_code) = 3
	GROUP BY state_code
) as si
ON si.state_code = LEFT(areas.cew_code, 2)