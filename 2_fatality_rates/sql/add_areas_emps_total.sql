UPDATE public.areas
SET emplvl_total = the_total
FROM (
	SELECT
		  area_fips
		, SUM(annual_avg_emplvl) as the_total
	FROM cew.annual_averages
	WHERE annual_averages.agglvl_code = 50
	GROUP BY area_fips
) as cew_data
WHERE cew_data.area_fips = areas.cew_code;