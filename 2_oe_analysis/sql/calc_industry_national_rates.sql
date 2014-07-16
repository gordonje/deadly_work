-- add columns
ALTER TABLE industries
ADD COLUMN fatals_rate numeric;

-- set values 
UPDATE industries 
SET fatals_rate = fatals_sum / emplvl_sum;
