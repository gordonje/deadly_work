Over-Expected Analysis
======================

1. [Calculate expected fatalities in each industry in each state](https://github.com/gordonje/deadly_work/blob/master/3_oe_analysis/sql/calc_expected_fatals.sql)

	Given industry's national fatality rate multiplied by the sum of the industry's employment level across all years in each state (from the [create_states_industries](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/create_states_industries.sql#L9) query)

2. [Calculate residual for each industry in each state](https://github.com/gordonje/deadly_work/blob/master/3_oe_analysis/sql/calc_states_industries_res.sql)

	Sum of fatalities for the given industry and state minus the expected fatalities for each industry and state

3. [Get NAICS 3 results](https://github.com/gordonje/deadly_work/blob/master/3_oe_analysis/sql/create_states_naics_3.sql)

	Include the [sum of employment levels](https://github.com/gordonje/deadly_work/blob/master/3_oe_analysis/sql/create_states_naics_3.sql#L10) (across all industries)

	Include the [sum of fatalities](https://github.com/gordonje/deadly_work/blob/master/3_oe_analysis/sql/create_states_naics_3.sql#L10) (across all industries)

	[Sum the expected fatalities](https://github.com/gordonje/deadly_work/blob/master/3_oe_analysis/sql/create_states_naics_3.sql#L23) for each state

	[Calculate residual](https://github.com/gordonje/deadly_work/blob/master/3_oe_analysis/sql/create_states_naics_3.sql#L16) (total fatalities - expected fatalities)
	
	Do all of this [only for the 3-digit NAICS industries](https://github.com/gordonje/deadly_work/blob/master/3_oe_analysis/sql/create_states_naics_3.sql#L26)

6. [Calculate adjusted rate for each state](https://github.com/gordonje/deadly_work/blob/master/3_oe_analysis/sql/calc_states_adj_fatal_rate.sql)

	State's residual divided by the state's total employment level


Run oe_analysis.py to complete these steps.