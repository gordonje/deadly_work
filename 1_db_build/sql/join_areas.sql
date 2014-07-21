CREATE TABLE areas
AS
	SELECT 
		  cew_areas.code as cew_code
		, cew_areas.title as cew_name
		, cfoi_areas.area_code as cfoi_code
		, cfoi_areas.area_text as cfoi_name
	FROM cew.areas as cew_areas
	JOIN (
		SELECT *
		FROM fi.area
		UNION
		SELECT *
		FROM fw.area
	) as cfoi_areas
	ON right(cfoi_areas.area_code, 2) || '000' = cew_areas.code
	AND cfoi_areas.area_code LIKE 'S%';

-- fix New York State's record
UPDATE areas
SET
	  cfoi_code = 'S69'
	, cfoi_name = 'New York State and New York City'
WHERE cew_code = '36000';

-- manual map Puerto Rico
INSERT INTO areas (cew_code, cew_name, cfoi_code, cfoi_name)
VALUES ('72000', 'Puerto Rico -- Statewide', 'S43', 'Puerto Rico');

-- 
CREATE INDEX areas_cew_code_ind ON areas (cew_code);

CREATE INDEX areas_cfoi_code_ind ON areas (cfoi_code);