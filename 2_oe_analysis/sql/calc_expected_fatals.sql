ALTER TABLE states_industries
ADD COLUMN expect_fatals numeric;


UPDATE states_industries
SET 
-- formula for expected fatals: 
-- state industries employment level multipled by the nationl rate for the industry
	  expect_fatals = states_industries.emplvl_sum * industries.fatals_rate
FROM industries
WHERE states_industries.industry_code = industries.cew_code
	AND states_industries.fatals_sum > 0;