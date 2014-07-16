ALTER TABLE states_industries
ADD COLUMN residual numeric;

UPDATE states_industries
SET 
-- formula for residual: actual fatals minus expected fatals
residual = fatals_sum - expect_fatals;