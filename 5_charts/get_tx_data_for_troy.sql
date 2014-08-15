-- get Texas sector data
SELECT 
	  a.cew_code as naics_code
	, COALESCE(a.display_name, a.cfoi_name) as sector_display_name
	, a.cfoi_name as sector_full_name
	, ROUND(b.emplvl_sum / 10) as emplvl
	, ROUND(expect_fatals) as expected_fatals
	, ROUND(b.residual)::int as residual
	, a.sort_order
FROM industries a
JOIN states_industries b
ON a.cew_code = b.industry_code
WHERE a.display_level = 3 
AND a.cew_code NOT LIKE '1%%'
AND b.residual IS NOT NULL
AND b.state_code = '48'
ORDER BY 
	  a.sort_order DESC;

-- get five worst Texas construction industry data
SELECT 
	  a.cew_code as naics_code
	, a.cfoi_name as industry
	, ROUND(b.emplvl_sum / 10) as emplvl
	, ROUND(expect_fatals) as expected_fatals
	, ROUND(b.residual)::int as residual
FROM industries a
JOIN states_industries b
ON a.cew_code = b.industry_code
WHERE b.industry_code in ('23821', '23816', '23814', '23813', '23712')
AND b.residual IS NOT NULL
AND b.state_code = '48'
ORDER BY 
	  b.residual DESC;

-- get five worst Texas oil and gas related data
SELECT 
	  a.cew_code as naics_code
	, a.cfoi_name as industry
	, ROUND(b.emplvl_sum / 10) as emplvl
	, ROUND(expect_fatals) as expected_fatals
	, ROUND(b.residual)::int as residual
FROM industries a
JOIN states_industries b
ON a.cew_code = b.industry_code
WHERE b.industry_code in ('21111', '22121', '48621', '32512', '33313', '42381', '48611')
AND b.residual IS NOT NULL
AND b.state_code = '48'
ORDER BY 
	  b.residual DESC;