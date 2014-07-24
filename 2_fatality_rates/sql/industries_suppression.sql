CREATE TABLE industries_suppression
AS
	SELECT
		  cfoi_inds.industry_code
		, cfoi_inds.industry
		, national.fatals_sum as national_fatals_total
		, states.fatals_sum as states_fatals_sum
		, (states.fatals_sum / national.fatals_sum) * 100 as pct_coverage
		, industries.all_states_count
		, industries.fatal_states_count
	FROM (
		SELECT 
			  industry_code
			, initcap(industry_text) as industry
			, display_level
		FROM fw.industry
		UNION
		SELECT 
			  industry_code
			, initcap(industry_text) as industry
			, display_level
		FROM fi.industry
	) cfoi_inds
	JOIN (
		SELECT
			  industry_code
			, CAST(SUM(fatals) as numeric) as fatals_sum
		FROM cfoi_data
		WHERE area_code = 'N00'
		GROUP BY industry_code
	) national
	ON cfoi_inds.industry_code = national.industry_code
	JOIN (
		SELECT
			  industry_code
			, CASE
				WHEN SUM(fatals) IS NULL THEN 0
				ELSE CAST(SUM(fatals) as numeric) 
			  END as fatals_sum
		FROM states_industries_years
		GROUP BY industry_code
	) as states
	ON TRIM(TRAILING 'X' FROM cfoi_inds.industry_code) = states.industry_code
	JOIN industries
	  ON industries.cfoi_code = national.industry_code
	ORDER BY states.fatals_sum / national.fatals_sum, cfoi_inds.industry_code;