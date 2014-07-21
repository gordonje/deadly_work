UPDATE industries
SET fatals_total = the_total
FROM (
-- we get the national numbers from the raw data, because there is less likely to be any suppression
	SELECT
		  industry_code
		, SUM(fatals) as the_total
	FROM cfoi_data
	WHERE area_code = 'N00'
	GROUP BY industry_code
) cfoi_data
WHERE industries.cfoi_code = cfoi_data.industry_code;