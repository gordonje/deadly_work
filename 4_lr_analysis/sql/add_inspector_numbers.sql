-- trim whitespace
UPDATE osha.inspectors_per_state
SET 
	state = trim(state)
, employees_number = trim(employees_number)
, inspectors_number = trim(inspectors_number)
, inspectors_needed = trim(inspectors_needed)
, inspect_empl_ratio = trim(inspect_empl_ratio);

-- convert to from string to int
ALTER TABLE osha.inspectors_per_state
	ALTER COLUMN employees_number SET DATA TYPE int8 USING cast(replace(employees_number, ',', '') as int)
, ALTER COLUMN inspectors_number SET DATA TYPE int8 USING cast(replace(inspectors_number, ',', '') as int)
, ALTER COLUMN inspectors_needed SET DATA TYPE int8 USING cast(replace(inspectors_needed, ',', '') as int)
;

-- add column to areas
ALTER TABLE states
ADD COLUMN inspectors int8;

-- set the inspector_number value on areas
UPDATE states
SET inspectors = inspectors_per_state.inspectors_number
FROM osha.inspectors_per_state
WHERE state_name = inspectors_per_state.state;


-- add states columns for calculated inspector to emplvl rate
ALTER TABLE states
ADD COLUMN insptrs_per_100k_emp numeric;

UPDATE states
SET insptrs_per_100k_emp = (inspectors / emplvl_sum) 