ALTER TABLE states
ADD COLUMN inspects_per_100k numeric,
ADD COLUMN inspects_per_100k_avg numeric;

UPDATE states
SET 
	  inspects_per_100k = the_rate
	, inspects_per_100k_avg = the_avg
FROM (
	SELECT
		  state_code
		, (SUM(insp_count) / SUM(emplvl_sum)) * 100000 as the_rate
		, AVG(inspects_rate * 100000) as the_avg
	FROM states_years
	GROUP BY state_code
) as styr
WHERE styr.state_code = states.state_code;