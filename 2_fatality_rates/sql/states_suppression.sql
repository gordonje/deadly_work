CREATE TABLE states_suppression
AS
	SELECT
		  areas.cfoi_code
		, areas.cfoi_name as state
		, lvl_0.fatals_sum as all_fatals
		, lvl_1.fatals_sum as lvl_1_fatals_sum
		, lvl_2.fatals_sum as lvl_2_fatals_sum
		, lvl_3.fatals_sum as lvl_3_fatals_sum
		, lvl_4.fatals_sum as lvl_4_fatals_sum
		, lvl_5.fatals_sum as lvl_5_fatals_sum
		, lvl_6.fatals_sum as lvl_6_fatals_sum
		, (lvl_1.fatals_sum / lvl_0.fatals_sum) * 100 as lvl_1_pct_cover
		, (lvl_2.fatals_sum / lvl_0.fatals_sum) * 100 as lvl_2_pct_cover
		, (lvl_3.fatals_sum / lvl_0.fatals_sum) * 100 as lvl_3_pct_cover
		, (lvl_4.fatals_sum / lvl_0.fatals_sum) * 100 as lvl_4_pct_cover
		, (lvl_5.fatals_sum / lvl_0.fatals_sum) * 100 as lvl_5_pct_cover
		, (lvl_6.fatals_sum / lvl_0.fatals_sum) * 100 as lvl_6_pct_cover
	FROM areas
	JOIN (
		SELECT
			  area_code
			, CAST(SUM(fatals) as numeric) as fatals_sum
		FROM cfoi_data
		JOIN (
			SELECT industry_code, display_level
			FROM fw.industry
			UNION
			SELECT industry_code, display_level
			FROM fi.industry	
		) as industries
		ON cfoi_data.industry_code = industries.industry_code
		WHERE display_level = 0
		GROUP BY area_code
		ORDER BY area_code
	) as lvl_0
	ON areas.cfoi_code = lvl_0.area_code
	JOIN (	
		SELECT
			  area_code
			, CAST(SUM(fatals) as numeric) as fatals_sum
		FROM cfoi_data
		JOIN (
			SELECT industry_code, display_level
			FROM fw.industry
			UNION
			SELECT industry_code, display_level
			FROM fi.industry	
		) as industries
		ON cfoi_data.industry_code = industries.industry_code
		WHERE display_level = 1
		GROUP BY area_code
		ORDER BY area_code
	) as lvl_1
	ON areas.cfoi_code = lvl_1.area_code
	JOIN (	
		SELECT
			  area_code
			, CAST(SUM(fatals) as numeric) as fatals_sum
		FROM cfoi_data
		JOIN (
			SELECT industry_code, display_level
			FROM fw.industry
			UNION
			SELECT industry_code, display_level
			FROM fi.industry	
		) as industries
		ON cfoi_data.industry_code = industries.industry_code
		WHERE display_level = 2
		GROUP BY area_code
		ORDER BY area_code
	) as lvl_2
	ON areas.cfoi_code = lvl_2.area_code
	JOIN (	
		SELECT
			  area_code
			, CAST(SUM(fatals) as numeric) as fatals_sum
		FROM cfoi_data
		JOIN (
			SELECT industry_code, display_level
			FROM fw.industry
			UNION
			SELECT industry_code, display_level
			FROM fi.industry	
		) as industries
		ON cfoi_data.industry_code = industries.industry_code
		WHERE display_level = 3
		GROUP BY area_code
		ORDER BY area_code
	) as lvl_3
	ON areas.cfoi_code = lvl_3.area_code
	JOIN (	
		SELECT
			  area_code
			, CAST(SUM(fatals) as numeric) as fatals_sum
		FROM cfoi_data
		JOIN (
			SELECT industry_code, display_level
			FROM fw.industry
			UNION
			SELECT industry_code, display_level
			FROM fi.industry	
		) as industries
		ON cfoi_data.industry_code = industries.industry_code
		WHERE display_level = 4
		GROUP BY area_code
		ORDER BY area_code
	) as lvl_4
	ON areas.cfoi_code = lvl_4.area_code
	JOIN (	
		SELECT
			  area_code
			, CAST(SUM(fatals) as numeric) as fatals_sum
		FROM cfoi_data
		JOIN (
			SELECT industry_code, display_level
			FROM fw.industry
			UNION
			SELECT industry_code, display_level
			FROM fi.industry	
		) as industries
		ON cfoi_data.industry_code = industries.industry_code
		WHERE display_level = 5
		GROUP BY area_code
		ORDER BY area_code
	) as lvl_5
	ON areas.cfoi_code = lvl_5.area_code
	JOIN (	
		SELECT
			  area_code
			, CAST(SUM(fatals) as numeric) as fatals_sum
		FROM cfoi_data
		JOIN (
			SELECT industry_code, display_level
			FROM fw.industry
			UNION
			SELECT industry_code, display_level
			FROM fi.industry	
		) as industries
		ON cfoi_data.industry_code = industries.industry_code
		WHERE display_level = 6
		GROUP BY area_code
		ORDER BY area_code
	) as lvl_6
	ON areas.cfoi_code = lvl_6.area_code
;