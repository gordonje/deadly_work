-- create table
CREATE TABLE industries
AS
	SELECT 
			cew_industries.code as cew_code
		  , cew_industries.title as cew_name
		  , cfoi_industries.industry_code as cfoi_code
		  , cfoi_industries.cfoi_name
		  , cfoi_industries.display_level
	FROM cew.industries as cew_industries
	JOIN (
-- use initcap() on industry_text to make PostgreSQL ignore the character case distinctions
		SELECT industry_code, initcap(industry_text) as cfoi_name, display_level
		FROM fw.industry
		UNION
		SELECT industry_code, initcap(industry_text) as cfoi_name, display_level
		FROM fi.industry
	) AS cfoi_industries
	ON cew_industries.code = trim(TRAILING 'X' FROM cfoi_industries.industry_code)
;

-- add indexes
CREATE INDEX industries_cew_code_ind ON industries (cew_code);

CREATE INDEX industries_cfoi_code_ind ON industries (cfoi_code);