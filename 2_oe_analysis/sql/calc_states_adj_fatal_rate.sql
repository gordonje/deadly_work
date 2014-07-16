ALTER TABLE states_NAICS_3
ADD COLUMN fatals_per_100k_adj numeric;

UPDATE states_NAICS_3
SET
-- formula for adjusted rate: state's residual divided by state's employment level
fatals_per_100k_adj = (residual / emplvl_sum) * 100000;