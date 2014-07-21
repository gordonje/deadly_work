-- create table 
CREATE TABLE states_industries_years
AS
	SELECT
		  LEFT(areas.cew_code, 2) as state_code
		, industries.cew_code as industry_code
		, annual_averages.year
		, cfoi_data.fatals
		, annual_averages.annual_avg_emplvl as emplvl
		, annual_averages.annual_avg_estabs_count as estabs
		, annual_averages.total_annual_wages
		, annual_averages.taxable_annual_wages
		, annual_averages.annual_contributions
		, annual_averages.annual_avg_wkly_wage
		, annual_averages.avg_annual_pay
		, CASE
				WHEN annual_averages.annual_avg_emplvl = 0 THEN NULL
				WHEN cfoi_data.fatals IS NULL THEN NULL
				ELSE cfoi_data.fatals / annual_averages.annual_avg_emplvl
			END as fatals_rate
	FROM (
			SELECT 
				  area_fips
				, industry_code
				, year 
				, SUM(annual_avg_estabs_count) as annual_avg_estabs_count
				, SUM(annual_avg_emplvl) as annual_avg_emplvl
				, SUM(total_annual_wages) as total_annual_wages
				, SUM(taxable_annual_wages) as taxable_annual_wages
				, SUM(annual_contributions) as annual_contributions
				, SUM(annual_avg_wkly_wage) as annual_avg_wkly_wage
				, SUM(avg_annual_pay) as avg_annual_pay
			FROM cew.annual_averages
-- we sum for non-overlapping sectors: Private and Government (Local, State, Federal and International)
			WHERE own_code >= 1
			AND own_code <= 5
-- also, narrow to the state and industry aggregation level
			AND agglvl_code >= 55
			AND agglvl_code <= 58
			GROUP BY 
				  area_fips
				, industry_code
				, year
		) AS annual_averages
	JOIN industries
		ON annual_averages.industry_code = industries.cew_code
	JOIN areas
		ON annual_averages.area_fips = areas.cew_code
-- left join, because we want to include industry/state/year combos without fatalities
	LEFT JOIN cfoi_data 
		ON industries.cfoi_code = cfoi_data.industry_code
		AND areas.cfoi_code = cfoi_data.area_code
		AND cfoi_data.year = annual_averages.year
;

-- add indexes
CREATE INDEX siy_state_code_ind ON states_industries_years (state_code);

CREATE INDEX siy_industry_code_ind ON states_industries_years (industry_code);

CREATE INDEX siy_year_ind ON states_industries_years (year);

CREATE INDEX siy_fatals_ind ON states_industries_years (fatals);

CREATE INDEX siy_emplvl_ind ON states_industries_years (emplvl);

CREATE INDEX siy_estabs_ind ON states_industries_years (estabs);

CREATE INDEX siy_state_industry_year ON states_industries_years (state_code, industry_code, year);