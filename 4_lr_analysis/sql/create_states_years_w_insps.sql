-- create states_years table
CREATE TABLE states_years 
AS
	SELECT
		  states.state_code
		, siy.year
		, siy.estabs_sum
		, siy.emplvl_sum
		, siy.fatals_sum
		, siy.fatals_rate
		, inspects.the_count as insp_count
		, inspects.the_count / siy.emplvl_sum as inspects_rate
	FROM states
	JOIN (
		SELECT 
				state_code
			, year
			, SUM(estabs) as estabs_sum
			, SUM(emplvl) as emplvl_sum
			, SUM(fatals) as fatals_sum
			, CASE 
					WHEN SUM(fatals) IS NULL THEN 0
					ELSE SUM(fatals) / SUM(emplvl)
				END as fatals_rate
		FROM states_industries_years
		WHERE CAST(industry_code as numeric) < 200
			AND char_length(industry_code) = 3
		GROUP BY 
				state_code
			, year
	) as siy
	ON siy.state_code = states.state_code
-- straight join is fine, as there aren't states in these results with fewer than 10 years
	JOIN (
		SELECT 
				site_state
			, open_year
			, COUNT(*) as the_count
		FROM osha.inspections
-- narrow to our fatal and emp data's time frame
		WHERE open_year >= 2003
			AND open_year <= 2012
-- also filter out the agri related inspections
			AND naics_code NOT LIKE '1%'
		GROUP BY 	
				site_state
			, open_year
		ORDER BY 	
				site_state
			, open_year
	) as inspects
	ON inspects.site_state = states.abbrv
	AND inspects.open_year = siy.year;

-- add indexes
CREATE INDEX states_years_code_ind ON states_years (state_code);

CREATE INDEX states_years_year_ind ON states_years (year);

CREATE INDEX states_years_industry_year_ind ON states_years (state_code, year);

CREATE INDEX states_years_fatals_ind ON states_years (fatals_sum);

CREATE INDEX states_years_emps_ind ON states_years (emplvl_sum);

CREATE INDEX states_years_fatal_rate_ind ON states_years (fatals_rate);

CREATE INDEX states_years_insp_rate_ind ON states_years (inspects_rate);

