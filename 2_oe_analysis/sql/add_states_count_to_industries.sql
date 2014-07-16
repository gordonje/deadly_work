ALTER TABLE industries
ADD COLUMN states_count numeric;

UPDATE industries
SET states_count = the_count
FROM (
	SELECT
			industry_code
		, COUNT(*) as the_count
	FROM states_industries
	WHERE emplvl_sum > 0
	GROUP BY industry_code
) states_industries
WHERE states_industries.industry_code = industries.cew_code;