workplace_fatalities
====================

This repository contains code and explanations for an investigation of fatal occupational injuries. The goal was to compare state performance in this area while controlling for confounding factors, such as each state's employment level and the kinds of industries in which each state's workers are employed. We then tested several state-level factors (e.g., the number of OSHA inspections per 100k employees) for any statistically significant correlations with our risk-adjusted fatality rate.

Generally (so far) the process has involved:

1.	Aligning raw annual employment levels with annual fatality numbers for each available state, industry and year (outlined further in [1_db_build](https://github.com/gordonje/deadly_work/tree/master/1_db_build)).

2.	Calcultating a per worker fatality rate at different levels of detail, including:

*	The fatality rate for each state across all industries
*	The fatality rate for each industry across all states
*	The fatality rate for a given industry in each state

With this third fatality rate, we rank states from highest to lowest fatality rate within each industry, then count the number of industries in which each state had one of the five worst fatality rates and the number of times it had the worst fatality rate (outlined further in [2_fatality_rates](https://github.com/gordonje/deadly_work/tree/master/2_fatality_rates)).

3.	For each industry, calculating the expected number of deaths in a given state based on the industry's national fatality rate and the sum of the state's workers in that industry. Then, for each state, adding up the expected deaths across all industries and calculating a risk-adjusted fatality rate (outlined further in [3_oe_analysis](https://github.com/gordonje/deadly_work/tree/master/3_oe_analysis)).

4.	Adding to our database whatever state-level factors we suspected could correlate with our risk-adjusted fatality rate, then running linear regressions in order to test for any statistically significant correlations (outlined further in [4_lr_analysis](https://github.com/gordonje/deadly_work/tree/master/4_lr_analysis)).

Dependencies
------------

*   [Python 2.7](https://www.python.org/) 
*   [PostgreSQL 9.3](http://www.postgresql.org/)
*   [Psycopg 2](http://initd.org/psycopg/)
*	[R](http://www.r-project.org/)

