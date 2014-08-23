-- add states_years columns
ALTER TABLE states_years
ADD COLUMN pct_union_mems numeric,
ADD COLUMN pct_union_repd numeric;

-- set the percentage members column
UPDATE states_years
SET 
		pct_union_mems = mems_pct
FROM (
	SELECT 
			series.fips_code
		, all_data.year
		, all_data.value as mems_pct
	FROM lu.series
	JOIN lu.all_data
	ON all_data.series_id = series.series_id
	WHERE series.ages_code = '00'
		AND series.class_code = '16'
		AND series.earn_code = '00'
		AND series.education_code = '00'
		AND series.indy_code = '0000'
		AND series.lfst_code = '20'
		AND series.occupation_code	= '0000'
		AND series.orig_code	= '00'
-- change to '00' for whole numbers 
		AND series.pcts_code	= '05'
		AND series.race_code	= '00'
		AND series.seasonal	= 'U'
		AND series.sexs_code = '0'
		AND series.fips_code <> '00'
-- change to '00' for whole numbers 
		AND series.tdata_code = '01'
--change the union affiliation code
		AND series.unin_code = '1'
) as unions
WHERE unions.fips_code = states_years.state_code
	AND unions.year = states_years.year;

-- set the percentage represented column
UPDATE states_years
SET 
		pct_union_repd = repd_pct
FROM (
	SELECT 
			series.fips_code
		, all_data.year
		, all_data.value as repd_pct
	FROM lu.series
	JOIN lu.all_data
	ON all_data.series_id = series.series_id
	WHERE series.ages_code = '00'
		AND series.class_code = '16'
		AND series.earn_code = '00'
		AND series.education_code = '00'
		AND series.indy_code = '0000'
		AND series.lfst_code = '20'
		AND series.occupation_code	= '0000'
		AND series.orig_code	= '00'
-- change to '00' for whole numbers 
		AND series.pcts_code	= '05'
		AND series.race_code	= '00'
		AND series.seasonal	= 'U'
		AND series.sexs_code = '0'
		AND series.fips_code <> '00'
-- change to '00' for whole numbers 
		AND series.tdata_code = '01'
-- change the union affiliation code
		AND series.unin_code = '2'
) as unions
WHERE unions.fips_code = states_years.state_code
	AND unions.year = states_years.year;

-- add columns to states table for average pct union mems and repd
ALTER TABLE states
ADD COLUMN pct_union_mems_avg numeric,
ADD COLUMN pct_union_repd_avg numeric;

UPDATE states
SET 
	  pct_union_mems_avg = mems_avg
	, pct_union_repd_avg = repd_avg
FROM (
	SELECT
		  state_code
		, AVG(pct_union_mems) as mems_avg
		, AVG(pct_union_repd) as repd_avg
	FROM states_years
	GROUP BY state_code
	) as styr
WHERE styr.state_code = states.state_code;


