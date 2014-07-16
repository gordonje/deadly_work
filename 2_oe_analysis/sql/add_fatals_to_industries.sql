ALTER TABLE industries
ADD COLUMN fatals_sum numeric;

UPDATE industries
SET fatals_sum = the_sum
FROM (
	SELECT
			industry_code
		, SUM(fatals) as the_sum
	FROM cfoi_data
	WHERE area_code = 'N00'
-- double-check why
		AND industry_code <> '00'
	GROUP BY industry_code
) cfoi_data
WHERE industries.cfoi_code = cfoi_data.industry_code;