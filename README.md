workplace_fatalities
====================

This repository contains code and explanations for an investigation of fatal occupational injuries. The goal of the project was to compare state performance in this area while controlling for confounding factors, such as each state's employment level and the kinds of industries in which each state's workers are employed. We then tested several state-level factors (e.g., the number of OSHA inspections per 100k employees) for any statistically significant correlations with our risk-adjusted fatality rate.

Generally (so far) the process has involved:

1.	Aligning raw annual employment levels with fatality numbers for each state, industry and year they were available (outlined further in [1_db_build]()).
2.	For each industry, calculating each state's fatality rate across the decade, ranking states from highest to lowest fatality rate within each industry, then counting the number of industries in which each state had one of the five worst fatality rates and the number of times it had the worst fatality rate (outlined further in [2_state_ind_rates]()).
3.	For each industry, calculating the expected number of deaths in a given state based on the industry's national average fatality rate and the sum of the state's workers in that industry. Then, for each state, calculating a risk-adjusted fatality rate (outlined further in [3_oe_analysis]()).
4.	Adding to our database whatever state-level factors we suspected could correlate with our risk-adjusted fatality rate, then running linear regressions in order to test for any statistically significant correlations (outlined further in [4_lr_analysis]()).	

Dependencies
------------

*   [Python 2.7](https://www.python.org/) 
*   [PostgreSQL 9.3](http://www.postgresql.org/)
*   [Psycopg 2](http://initd.org/psycopg/)
*	[R](http://www.r-project.org/)

