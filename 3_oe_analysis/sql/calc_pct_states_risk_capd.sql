UPDATE states_naics_3
SET
-- formula for percentage of industry risk captured:
-- sum of captured employment levels (emplvl sum across all years in which some fatalites were reported)
-- divided by the state's total employment level (without any filtering)
pct_risk_capd = (emplvl_capd / emplvl_total) * 100



-- FROM (
--         SELECT 
--               state_code
--             , SUM(emplvl) as emplvl_sum
--         FROM public.states_industries_years
--         WHERE CHAR_LENGTH(industry_code) = 3
--         GROUP BY states_industries_years.state_code
-- ) as raw
-- WHERE raw.state_code = states_naics_3.state_code;