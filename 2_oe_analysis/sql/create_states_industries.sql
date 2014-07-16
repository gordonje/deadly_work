-- create table
CREATE TABLE states_industries
AS
	SELECT
			industry_code
		, state_code
		, SUM(estabs) as estabs_sum
		, SUM(emplvl) as emplvl_sum
		, SUM(fatals) as fatals_sum
		, CASE 
				WHEN SUM(emplvl) = 0 THEN NULL
				WHEN SUM(fatals) IS NULL THEN NULL
				ELSE SUM(fatals) / SUM(emplvl)
			END as fatals_rate_unadj
	FROM states_industries_years
		GROUP BY 		
			industry_code
		, state_code
;


-- add indexes
CREATE INDEX states_industries_industry_ind ON states_industries (industry_code);

CREATE INDEX states_industries_state_ind ON states_industries (state_code);

CREATE INDEX states_industries_industry_state_ind ON states_industries (industry_code, state_code);

CREATE INDEX states_industries_estabs_sum_ind ON states_industries (estabs_sum);

CREATE INDEX states_industries_fatals_sum_ind ON states_industries (fatals_sum);

CREATE INDEX states_industries_emps_sum_ind ON states_industries (fatals_rate_unadj);