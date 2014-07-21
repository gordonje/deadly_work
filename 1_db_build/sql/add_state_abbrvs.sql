UPDATE areas
SET abbrv = state_fips_to_abbrv.Abbrv
FROM state_fips_to_abbrv
WHERE LEFT(cew_code, 2) = state_fips_to_abbrv.FIPS;