-- create table
CREATE TABLE states_industries
AS
	SELECT
		  state_code
		, industry_code
		, COUNT(*) as years_count
		, SUM(estabs) as estabs_sum
		-- get this without suppression
		, SUM(emplvl) as emplvl_sum
		, SUM(fatals) as fatals_sum
		, CASE 
				WHEN SUM(emplvl) = 0 THEN NULL
				WHEN SUM(fatals) IS NULL THEN NULL
				ELSE (SUM(fatals) / SUM(emplvl)) * 100000
			END as fatals_per_100k
	FROM states_industries_years
	-- WHERE fatals IS NOT NULL
	--   AND emplvl > 0
	GROUP BY 		
		  state_code
		, industry_code
;


-- add indexes
CREATE INDEX states_industries_industry_ind ON states_industries (industry_code);

CREATE INDEX states_industries_state_ind ON states_industries (state_code);

CREATE INDEX states_industries_industry_state_ind ON states_industries (industry_code, state_code);

CREATE INDEX states_industries_estabs_sum_ind ON states_industries (estabs_sum);

CREATE INDEX states_industries_fatals_sum_ind ON states_industries (fatals_sum);

CREATE INDEX states_industries_emps_sum_ind ON states_industries (fatals_per_100k);