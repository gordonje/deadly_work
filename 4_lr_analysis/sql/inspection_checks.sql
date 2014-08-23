-- there are inspection records without an open_year value, but the other date values suggest these are from the 1980s
SELECT *
FROM osha.inspections
WHERE open_year is NULL;

-- there are 199 inspection records without a NAICS within our time period, so we probably shouldn't sum the inspectors for each industry
SELECT *
FROM osha.inspections
WHERE naics_code is NULL
AND open_year >= 2003
AND open_year <= 2012;

-- but we probably need to filter down to just the non-agri inspections, because there are quite a few in our time frame
SELECT naics_code, COUNT(*)
FROM osha.inspections
WHERE open_year >= 2003
	AND open_year <= 2012
GROUP BY naics_code
ORDER BY naics_code;

-- every state has at least one inspection for each of the ten years
SELECT site_state, count(*)
FROM 
(
		SELECT 
				site_state
			, open_year
			, COUNT(*) as the_count
		FROM osha.inspections
-- narrow to our fatal and emp data's time frame
		WHERE open_year >= 2003
			AND open_year <= 2012
-- also filter out the agri related inspections
			AND naics_code NOT LIKE '1%'
		GROUP BY 	
				site_state
			, open_year
		ORDER BY 	
				site_state
			, open_year
	) as inspects
GROUP BY site_state
ORDER BY COUNT(*);