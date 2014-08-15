SELECT 
	  state_code as id
	, state_name as state
	, is_right_to_work as union
	, a.emplvl_total as emplys
	, a.fatals_total as actual_fatals
	, expect_fatals_sum as expected_fatals
	, residual
	, a.fatals_total / expect_fatals_sum as perform
	, a.fatals_per_100k_adj
FROM states_naics2_no_agri a
JOIN areas b
ON LEFT(cew_code, 2) = state_code
ORDER BY residual DESC;
