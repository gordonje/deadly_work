UPDATE industries
SET emplvl_total = the_total
FROM (
	SELECT
		  industry_code
		, SUM(annual_avg_emplvl) as the_total
	FROM cew.annual_averages
	WHERE agglvl_code >= 15
	AND agglvl_code <= 18
	GROUP BY industry_code
) as cew_data
WHERE cew_data.industry_code = industries.cew_code;