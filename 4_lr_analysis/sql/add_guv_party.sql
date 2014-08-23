UPDATE areas
SET is_dem_guv = '1'
FROM (
	SELECT state
	FROM public.governors
	WHERE party = 'D'
	GROUP BY state
	HAVING count(*) = 10
) guvs
WHERE guvs.state = CASE
						WHEN areas.cew_code = '11000' THEN areas.cew_name
						ELSE TRIM(LEFT(areas.cew_name, POSITION(' -' in areas.cew_name)))
					END
;


UPDATE areas
SET is_rep_guv = '1'
FROM (
	SELECT state
	FROM public.governors
	WHERE party = 'R'
	GROUP BY state
	HAVING count(*) = 10
) guvs
WHERE guvs.state = CASE
						WHEN areas.cew_code = '11000' THEN areas.cew_name
						ELSE TRIM(LEFT(areas.cew_name, POSITION(' -' in areas.cew_name)))
					END
;
