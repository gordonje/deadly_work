UPDATE states_naics2_w_agri
SET 
-- formula for adjusted rate: 
-- state's residual divided by sum of employment level (without industry filtering)
fatals_per_100k_adj = (residual / emplvl_total) * 100000;