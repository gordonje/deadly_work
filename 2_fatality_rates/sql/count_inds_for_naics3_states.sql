UPDATE states_naics_3
SET industries_count = sub1.the_count
FROM (
	SELECT
		  state_code
		, COUNT(*) as the_count
	FROM (
			SELECT
				  state_code
				, industry_code
				, SUM(emplvl)
			FROM states_industries_years
			-- exclude agri
			WHERE industry_code NOT LIKE '1%'
			-- narrow to 3-digit naics
			AND CHAR_LENGTH(industry_code) = 3
			GROUP BY 
				  state_code
				, industry_code
			-- only count industries in the state that actually employ people
			HAVING SUM(emplvl) > 0
		) as sub2
	GROUP BY state_code
	) as sub1
WHERE states_naics_3.state_code = sub1.state_code