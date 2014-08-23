ALTER table public.areas
ADD COLUMN pct_union_mems_avg numeric,
ADD COLUMN pct_union_repd_avg numeric;

UPDATE areas
SET 
	  pct_union_mems_avg = mems_avg
	, pct_union_repd_avg = repd_avg
FROM (
	SELECT
		  repd.fips_code
		, AVG(mems.pct) as mems_avg
		, AVG(repd.pct) as repd_avg
	FROM (
		SELECT 
			  series.fips_code
			, all_data.year
			, all_data.value as pct
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
	) mems
	JOIN (
		SELECT 
			  series.fips_code
			, all_data.year
			, all_data.value as pct
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
	) repd
	ON mems.fips_code = repd.fips_code
	AND mems.year = repd.year
	GROUP BY repd.fips_code
) unions
WHERE LEFT(areas.cew_code, 2) = unions.fips_code