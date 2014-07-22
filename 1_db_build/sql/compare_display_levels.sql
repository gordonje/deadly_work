SELECT 
	  display_level 
	, COUNT(*) as industries_count
	, SUM(fatals_sum) as fatals_sum
FROM (
	SELECT 
		  industry_code
		, SUM(fatals_sum) as fatals_sum
	FROM (
		SELECT 
			  industry_code
			, area_code
			, SUM(fatals) as fatals_sum
		FROM cfoi_data
		GROUP BY
			  industry_code
			, area_code
	) inds_areas
	GROUP BY industry_code
) inds
JOIN industries
ON industries.cfoi_code = inds.industry_code
GROUP BY display_level 
ORDER BY display_level;
