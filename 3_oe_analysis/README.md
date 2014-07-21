Over-Expected Analysis
======================

1. Calculate expected fatalities in each industry in each state
	** given industry's national fatality rate multiplied by the sum of the industry's employment level across all years where fatalities were reported in each state

2. Calculate residual for each industry in each state
	** sum of fatalities for the given industry and state minus the expected fatalities for each industry and state

3. Get NAICS 3 results
	** include the sum of employment levels (across all industries)
	** include the sum of captured employment levels (across all years and industries in which fatalities were reported)
	** include the sum of captured fatalities
	** sum the expected fatalities for each state
	** calculate residual (captured fatalities - expected fatalities)

6. Calculate adjusted rate for each state
	** Residual divided by the captured employment level

7. Calculate the percentage of industry risk captured
	** captured employment level divided by the total employment level

Run oe_analysis.py to complete these steps.