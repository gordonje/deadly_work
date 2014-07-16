-- returns no rows, confirming that series_ID and year are unique
SELECT 
	  series_id
	, year
	, COUNT(*)
FROM combined.cfoi_data
GROUP BY 
	  series_id
	, year
HAVING COUNT(*) > 1;
 
-- returns no rows, confirming that industry_code, area_code and year are unique
SELECT 
	  industry_code
	, area_code
	, year
	, COUNT(*)
FROM combined.cfoi_data
GROUP BY 
	  industry_code
	, area_code
	, year
HAVING COUNT(*) > 1;