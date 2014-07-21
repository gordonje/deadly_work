Unadjusted Fatality Rates
===================================

BLS Data Non-Disclosure
--------------------

Before we go further, we need to delve into the biggest gotcha in using this BLS data.

In a nutshell, BLS will not disclose either the number of fatalities in cases where that information is considered "personally identifiable". The policy is meant to prevent someone from figuring out exactly who died, which would be easier, for example if there are fewer deaths among fewer employees. BLS also will not disclose employment levels under similar circumstances, though the actual suppression rules for both datasets are intentionally opaque.

What makes this tricky for us is that BLS will either report a number or it won't without indicating when the non-disclosure rules were applied. For example, BLS may not report any electrical contractor deaths in Rhode Island in 2012, but we can't be certain whether there were a small number of deaths that weren't disclosed or if there in fact were no electical contractor deaths in Rhode Island in 2012.

However, the suppressed numbers are included at higher aggregation levels. So while we might not be certain of how many electrical contractor deaths happened in Rhode Island in 2012, we can at least trust that the eight deaths reported across the entire "Ocean State" in 2012 is an accurate number.

That means we can at least get some feel for how aggressively the non-disclosure rules are applied. We can [query](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/states_suppression.sql) to compare [how many deaths are reported in each state at each industry detail level](https://github.com/gordonje/deadly_work/blob/master/results/states_suppression.csv). For each industry, we can also [query](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/industries_suppression.sql) to [compare the industry's national fatality number to the sum of fatalities across the states](https://github.com/gordonje/deadly_work/blob/master/results/industries_suppression.csv). 

For our purposes, the most important take-aways are:

1.	Where we can, we use the total fatalities and employment levels published by BLS at the higher aggregation level, rather than doing our own sums of fatalities and employment levels.

2.	We need to be aware of how the results could be skewed in favor of larger states, which will tend to have more industries large enough to escape BLS' non-disclosure rules.

3.	There are some weird cases when -- in a given state, industry and year -- [BLS published the number of fatalities but not the employment level](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/deaths_but_no_emps.sql).


Calculating Unadjusted Rates
----------------------------

1. [Sum the total fatalities (across all industries) for each area](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/add_areas_fatals_total.sql)

2. [Sum the total employment levels (across all industries) for each area](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/add_areas_emps_total.sql)

3. [Calculate an unadjusted fatality rate per 100k workers for each area](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/calc_areas_unadj_fatal_rate.sql)

4. [Sum the national fatalities for each industry](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/add_industries_fatals_total.sql)

5. [Sum the national employment levels for each industry](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/add_industries_emps_total.sql)

6. Calculate [industry national fatality](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/calc_industry_national_rates.sql) rate per 100k workers

7.	[Create states_industries table](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/create_states_industries.sql)
	Group by state and industry
	
	Sum all fatalities across all years and all employment level across all years.
	
	Calculate a [fatality rate per 100k workers](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/create_states_industries.sql#L14)

8. 	Within each industry, [rank the states from highest to lowest fatality rate](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/rank_states_in_industries.sql)
	
	Only do this for state_industries with [at least 5 years worth of data](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/rank_states_in_industries.sql#L10)

9. [For each state, count the number of industries in which it is ranked the worst](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/count_areas_top1s.sql)
	
	Only count the times [when it's competiting with at least 1 other state](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/count_areas_top1s.sql#L12-L20)

10. [For each state, count the number of industries in which it is ranked one of the five worst](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/count_areas_top5s.sql)
	
	Only count the times [when it's competiting with at least five other states](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/sql/count_areas_top5s.sql#L12-L19)


Run [calc_fatal_rates_unadj.py](https://github.com/gordonje/deadly_work/blob/master/2_fatality_rates/calc_fatal_rates_unadj.py) to complete these steps.
	
