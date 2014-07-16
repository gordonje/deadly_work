Building the Database
=====================

Herein we explain how we acquired and joined together the raw employee and fatalities numbers for each available state, industry and year.

All this data was imported into a single PostgreSQL database. Since we were mashing together lots of data from multiple sources, we organized tables into several different [schemas](http://www.postgresql.org/docs/9.3/static/ddl-schemas.html), one for each of the data sources. The tables derived from this source data went into the "public" schema (PostgreSQL's default). You'll note, then, that queries against source tables will specify the schema in which it resides, while we ignore the schema when querying our derived tables.

Fatalities Data
---------------

First, we downloaded the text files for the past ten years of the [Census of Fatal Occupational Injuries](http://www.bls.gov/iif/oshfat1.htm). CFOI

CFOI is segmented into two databases: One for [2003 to 2010](http://download.bls.gov/pub/time.series/fi/) (prefix fi) and another for [2011 forward](http://download.bls.gov/pub/time.series/fw/) (prefix fw), which currently only contains 2011 and 2012.

Both databases contains two primary tables, one named 'all_data' and another named 'current_data'. The ReadMe file in each database describes the latter as containing "all current year-to-date data", but actually these tables [appear to be identical](). So we excluded the 'current_data' table from the rest of the workflow.

In order to make things a little easier query-wise, we created a [combined CFOI data table](https://github.com/gordonje/workplace_fatalities/blob/master/sql_scripts/combine_cfoi_data.sql) and populated it with the records of counts for "Total fatalities" (category_code '00X') and "Fatalities in all sectors" (case_code '0'). Note that the "all sectors" fatality count for each industry, area and year combination is often [slightly more](https://gist.github.com/gordonje/2d35d4cd451216f37966#file-all_vs_sum_sectors) than the sum of fatalities for the private (case_code 1) and all levels of government (case_code 9). But the difference is never more than four deaths, which are likely attributable to BLS' confidentiality policy.

Again, we need to get the numbers for each industry, state and year combination, so we ran a couple of [sanity checks]() to be sure there aren't any duplicate rows in this new table.

The [get_fw_data.py](https://github.com/gordonje/workplace_fatalities/blob/master/get_fw_data.py) and [get_fi_data.py](https://github.com/gordonje/workplace_fatalities/blob/master/get_fi_data.py) scripts in this repo will download and import the CFOI data, provided you've installed all of the [dependencies](https://github.com/gordonje/workplace_fatalities#dependencies) into your environment. Note that you must have a database named 'BLS' created ahead of time, and you will be prompted for your PostgreSQL username and password.

Employment Data
---------------

For the employment numbers, we tried working with multiple different databases before settling on the [Quarterly Census of Employment and Wages](http://www.bls.gov/cew/home.htm) (QCEW), which is more comprehensive than similar databases (like the Census of Employment Statistics (CES)) because the BLS collects the numbers directly from the establishments, and response is mandatory. Multiple economists from different BLS programs said QCEW was the way to go.

We downloaded the 2003 to 2012 annual average .csv files from [here](http://www.bls.gov/cew/datatoc.htm), and then imported each into a single annual_averages table. Initially, this gave us 36 million records, so the queries on this table were running rather slowly. But most of these records were for employment and wage data at the county- or metro- rather than the state-level. Since the CFOI's fatality numbers don't go beyond the state-level (save for a handful of large metro areas), we narrowed my CEW records to only the national- and state-level by [deleting](https://gist.github.com/gordonje/e91a6de9a5e089c6f734#file-delete_county_and_metro_cew) all the other records at some other [aggregation level](http://www.bls.gov/cew/doc/titles/agglevel/agglevel_titles.htm).

We also downloaded and imported all five of QCEW's look-up tables: [Industries](http://www.bls.gov/cew/doc/titles/industry/industry_titles.htm), [Areas](http://www.bls.gov/cew/doc/titles/area/area_titles.htm), [Ownerships](http://www.bls.gov/cew/doc/titles/ownership/ownership_titles.htm), [Size Classes](http://www.bls.gov/cew/doc/titles/size/size_titles.htm) and [Aggregation Levels](http://www.bls.gov/cew/doc/titles/agglevel/agglevel_titles.htm).

The [get_cew_data.py]() script in this repo will import the CEW into the BLS database (again, you must have the [dependencies](https://github.com/gordonje/workplace_fatalities#dependencies) installed and you have to provide your PostgreSQL username and password). Ahead of time, you'll also need to download and extract the annual average files to your current working directory.

Joining Fatality and Employment
-------------------------------

We started with the relevant look-up tables.

First, we [joined the areas](https://github.com/gordonje/workplace_fatalities/blob/master/sql_scripts/join_areas.sql) into a single table that contains a record for each state and one for the national level. Note that, in the case of New York State, the CFOI area_code labeled 'New York State (except NYC)' lines up to the CEW area_fips labeled 'New York -- Statewide', so I'm manually aligning to the 'S69' labeled 'New York State and New York City', which a CFOI economist said would be appropriate.

Then, we [joined industries](https://github.com/gordonje/workplace_fatalities/blob/master/sql_scripts/join_industries.sql) into a single table that contains only the industries included in both CFOI and CEW. Note that industry names in fi and fw use different character casing (e.g., 'Specialty trade contractors' versus 'Specialty Trade Contractors'), so we use the INITCAP() function to make PostgreSQL ignore this these distinctions.

A little more about industries: 

*	The NAICS codes representing them are nested, with very specific industries (e.g., "Natural gas liquid extraction" coded "211112") fitting under more general ones (e.g., "Oil and gas extraction" coded "211XXX"). These layers are called 'display_levels'.

* 	As you drill down into the more specific industries, [the total number of fatalities decreases]() by several thousand nationally, presumably because of fatalities not disclosed in more specific industries that are nonetheless included in aggregates of the more general industries.

We then used the aligned areas and industries to [join employee and fatalities counts](https://github.com/gordonje/workplace_fatalities/blob/master/sql_scripts/join_cfoi_to_cew.sql) into a single table. A couple of things to note about this query:

*	Since there are going to be years in which no one died in a particular state and industry (or there were too few to disclose), and we need to include the employment numbers for those year. Therefore, it's important to select the employment numbers first then [left join](https://github.com/gordonje/workplace_fatalities/blob/master/sql_scripts/join_cfoi_to_cew.sql#L53) to the fatality records.

*	Relatedly, we [replaced the NULL fatality values with a zero](https://github.com/gordonje/workplace_fatalities/blob/master/sql_scripts/join_cfoi_to_cew.sql#L8) in order to simplify things slightly. Actually, the CFOI data doesn't ever confirm that there were zero deaths in a particular state, industry and year. Rather, in the absence any number, we only know there were five or fewer deaths in that particular state, industry and year.

*   When CEW aggregates at the industry level, they also break down the numbers by sector (aka, [ownerships](http://www.bls.gov/cew/doc/titles/ownership/ownership_titles.htm)), so there isn't a record for Total Covered' (own_code 0) and ???. Instead, we [sum the numbers for the non-overlapping sectors](https://github.com/gordonje/workplace_fatalities/blob/master/sql_scripts/join_cfoi_to_cew.sql#L40) (i.e., own_codes 1 through 5).

Next Step
---------

With fatality and employment numbers imported and joined, we could then [summarize](https://github.com/gordonje/workplace_fatalities/tree/master/summarize_db) this data with descriptive stats.