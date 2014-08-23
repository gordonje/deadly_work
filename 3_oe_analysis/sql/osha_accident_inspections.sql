SELECT count(*)
FROM osha.inspections
WHERE site_state = 'TX'
AND insp_type = 'A'
AND open_year >= 2003
AND open_year <= 2012
AND naics_code NOT LIKE '1%'