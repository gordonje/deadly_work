CREATE TABLE states_naics2_no_agri
AS 
	SELECT
		  a.state_code
		, a.state_name
		, a.abbrv
		, a.emplvl_total - b.emplvl_sum as emplvl_total
		, a.fatals_total - b.fatals_sum as fatals_total
		, a.expect_fatals_sum - b.expect_fatals as expect_fatals_sum
	FROM states_naics2_w_agri a
	LEFT JOIN (
		SELECT 
			  state_code
			, CASE 
				WHEN emplvl_sum IS NULL THEN 0
				ELSE emplvl_sum
			  END as emplvl_sum
			, CASE 
				WHEN fatals_sum IS NULL THEN 0
				ELSE fatals_sum
			  END as fatals_sum
			, CASE
				WHEN expect_fatals IS NULL THEN 0
				ELSE expect_fatals
			  END as expect_fatals
		FROM states_industries
		WHERE industry_code = '11'
		) b
	ON a.state_code = b.state_code
;