SELECT
	*
FROM
	states_industries_years
WHERE
	fatals IS NOT NULL
AND emplvl = 0
ORDER BY
	state_code,
	industry_code,
	YEAR;