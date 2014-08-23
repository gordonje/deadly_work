ALTER TABLE states
ADD COLUMN is_right_to_work varchar(2) DEFAULT '0';

UPDATE areas
SET 
	is_right_to_work = '1'
FROM right_to_work
WHERE right_to_work.field1 = CASE
						WHEN areas.cew_code = '11000' THEN areas.cew_name
						ELSE TRIM(LEFT(areas.cew_name, POSITION(' -' in areas.cew_name)))
					END;