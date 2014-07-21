SELECT
	  industry_code
	, title as industry
	, SUM(annual_avg_emplvl) as the_sum
FROM cew.annual_averages
JOIN cew.industries
ON industries.code = annual_averages.industry_code
WHERE agglvl_code >= 15
AND agglvl_code <= 18
AND own_code >= 1
AND own_code <= 5
GROUP BY industry_code, title
HAVING industry_code not in (select cew_code from public.industries)
ORDER BY CHAR_LENGTH(industry_code), industry_code;