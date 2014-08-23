ALTER TABLE areas
ADD COLUMN insp_count numeric;

UPDATE areas
SET insp_count = the_count
FROM (
	SELECT 
		  site_state
		, COUNT(*) as the_count
	FROM osha.inspections
	-- narrow to our fatal and emp data's time frame
	WHERE open_year >= 2003
		AND open_year <= 2012
	-- also filter out the agri related inspections
		AND naics_code NOT LIKE '1%'
	GROUP BY 	
		  site_state
) as insp
WHERE insp.site_state = areas.abbrv;