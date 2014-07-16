ALTER TABLE industries
ADD COLUMN states_count int;

UPDATE industries
SET states_count = the_count
FROM (
	SELECT
		  industry_code
		, count(*) as the_count
	FROM states_industries
	WHERE emplvl_sum > 0
	GROUP BY industry_code
) as a
WHERE a.industry_code = industries.cew_code;