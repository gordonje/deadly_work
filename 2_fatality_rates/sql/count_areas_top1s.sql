UPDATE areas
SET top_1_count = the_count
FROM (
-- count the number of industries where each state has the worst fatality rates
	SELECT
		  state_code
		, COUNT(*) as the_count
	FROM states_industries
	WHERE state_rank = 1
-- and narrow to industries were there are two or more states 
-- with fatalities reported in five or more years (happenings in the query that applies the ranks)
	  AND industry_code IN (
			SELECT 
				  industry_code
			FROM states_industries
			GROUP BY 
				  industry_code
			HAVING 
				  MAX(state_rank) >= 2
	)
	GROUP BY 
		state_code
) as stind
WHERE LEFT(areas.cew_code, 2) = stind.state_code;