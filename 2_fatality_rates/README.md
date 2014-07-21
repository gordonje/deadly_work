Unadjusted Fatality Rates
===================================

BLS Data Suppression
--------------------

Before we go further, we need to delve into the biggest gotcha in using BLS data.

industries_suppression.sql

state_fatals_suppressed.sql

deaths_but_no_emps.sql


Calculating Unadjusted Rates
----------------------------

1. Sum the total fatalities (across all industries) for each area

2. Sum the total employment levels (across all industries) for each area

3. Calculate an unadjusted fatality rate per 100k workers for each area

4. Sum the national fatalities for each industry

5. Sum the national employment levels for each industry

6. Calculate industry national fatality rate per 100k workers

7.	Create states_industries table
	**	Group by state and industry
	**	Sum the fatalities and employment levels for years where fatalities were reported AND where an employment level was reported
	** Calculate a fatality rate per 100k workers

8. 	Within each industry, rank the states from highest to lowest fatality rate where the fatality rate is not NULL
	** Only do this for state_industries with at least 5 years worth of data

9. For each state, count the number of industries in which it is ranked the worst
	** Only count the times when it is competiting with at least 1 other state

10. For each state, count the number of industries in which it is ranked one of the five worst.
	** Only count the times when it is competiting with at least five other states

Run calc_fatal_rates_unadj.py to complete these steps.
	
