UPDATE public.areas
SET fatals_total = the_total
FROM (
	SELECT 
		  area_code
		, SUM(fatals) as the_total
	FROM cfoi_data
	WHERE industry_code = '000000'
	AND area_code like 'S%'
	GROUP BY area_code
	ORDER BY area_code
) as cfoi
WHERE areas.cfoi_code = cfoi.area_code;