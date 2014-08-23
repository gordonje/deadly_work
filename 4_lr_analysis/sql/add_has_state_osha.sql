UPDATE states
SET 
	has_osha = '1'
  , is_osha_public_sector_only = CASE WHEN osha_state_plans.public_sector_only THEN '1' ELSE '0' END
FROM combined.osha_state_plans
WHERE state_name = osha_state_plans.state;