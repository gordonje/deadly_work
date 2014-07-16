CREATE TABLE cfoi_data 
AS 
	SELECT 
		  alldata.series_id 
		, series.industry_code
		, series.area_code
		, alldata.year
		, alldata.value as fatals
	FROM fw.alldata
	JOIN fw.series
	ON series.series_id = alldata.series_id
-- narrow to "Fatalities in all sectors"
	WHERE series.case_code = '0'
-- and "Total fatalities"
	AND series.category_code = '00X'
	UNION
	SELECT 
		  alldata.series_id 
		, series.industry_code
		, series.area_code
		, alldata.year
		, alldata.value as fatals
	FROM fi.alldata
	JOIN fi.series
	ON series.series_id = alldata.series_id
-- narrow to "Fatalities in all sectors"
	WHERE series.case_code = '0'
-- and "Total fatalities"
	AND series.category_code = '00X';

-- add indexes
CREATE INDEX cfoi_series_id_ind ON cfoi_data (series_id);

CREATE INDEX cfoi_area_code_ind ON cfoi_data (area_code);

CREATE INDEX cfoi_industry_code_ind ON cfoi_data (industry_code);

CREATE INDEX cfoi_year_ind ON cfoi_data (year);

CREATE INDEX cfoi_value_ind ON cfoi_data (fatals);

CREATE INDEX cfoi_series_id_year_ind ON cfoi_data (series_id, year);

CREATE INDEX cfoi_area_code_industry_code_year_ind ON cfoi_data (area_code, series_id, year);