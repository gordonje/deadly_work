ALTER TABLE industries
ADD COLUMN emplvl_sum numeric;

UPDATE industries
SET emplvl_sum = the_sum
FROM (
	SELECT
			industry_code
		, SUM(emplvl_sum) as the_sum
	FROM states_industries
	GROUP BY industry_code
) states_industries
WHERE states_industries.industry_code = industries.cew_code;

-- get the national numbers from raw data