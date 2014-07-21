Building the Database
=====================

Herein we explain how we acquired and joined together the raw employee and fatalities numbers for each available state, industry and year.

All this data was imported into a single PostgreSQL database. Since we were mashing together lots of data from multiple sources, we organized tables into several different [schemas](http://www.postgresql.org/docs/9.3/static/ddl-schemas.html), one for each of the data sources. The tables derived from this source data went into the "public" schema (PostgreSQL's default). You'll note, then, that queries against source tables will specify the schema in which it resides, while we ignore the schema when querying our derived tables.


Fatalities Data
---------------

First, we downloaded the text files for the past ten years of the [Census of Fatal Occupational Injuries](http://www.bls.gov/iif/oshfat1.htm). 

CFOI is widely considered to be one of the most reliable sources of workplace fatalities because the program is a collaborative effort between federal and state agencies that obtain their information from multiple sources, including death certificates, workers compensation claims as well as reports from the Occupational Safety and Health Administration (OSHA). Each reported death is substantiated two or more independents source documents. 

The fatalities included in CFOI all result from traumatic injuries while engaged in for-pay or volunteer work. CFOI does not include fatalities caused by illness resulting from prolonged exposure, for example, to hazardous materials. A construction worker's death by falling from a great height would be counted. A miner's death from black lung would not. 

You can read more in Part III of [this chapter from BLS' Handbook of Methods](http://www.bls.gov/opub/hom/pdf/homch9.pdf).

CFOI is segmented into two databases: One for [2003 to 2010](http://download.bls.gov/pub/time.series/fi/) (prefix fi) and another for [2011 forward](http://download.bls.gov/pub/time.series/fw/) (prefix fw), which currently only contains 2011 and 2012.

Both databases contains two primary tables, one named 'all_data' and another named 'current_data'. The ReadMe file in each database describes the latter as containing "all current year-to-date data", but actually these tables [appear to be identical](https://github.com/gordonje/deadly_work/blob/master/1_db_build/sql/compare_alldata_to%20current.sql). So we excluded the 'current_data' table from the rest of the workflow.

In order to make things a little easier query-wise, we created a [combined CFOI data table](https://github.com/gordonje/deadly_work/blob/master/1_db_build/sql/combine_cfoi_data.sql) and populated it with the records of counts for "Total fatalities" (category_code '00X') and "Fatalities in all sectors" (case_code '0'). 

Again, we need to get the numbers for each industry, state and year combination, so we ran a couple of [sanity checks](https://github.com/gordonje/deadly_work/blob/master/1_db_build/sql/no_cfoi_dupes.sql) to be sure there aren't any duplicate rows in this new table.

The [get_cfoi_data.py](https://github.com/gordonje/deadly_work/blob/master/1_db_build/get_cfoi_data.py) script in this repo will download and import the CFOI data into any database on your local PostgreSQL server, provided you've installed all of the [dependencies](https://github.com/gordonje/deadly_work#dependencies) into your environment. You'll be prompted for the database's name, your PostgreSQL username and password.


Employment Data
---------------

For the employment numbers, we tried working with multiple different databases before settling on the [Quarterly Census of Employment and Wages](http://www.bls.gov/cew/home.htm) (QCEW), which is more comprehensive than similar databases (like the Census of Employment Statistics (CES)) because the BLS collects the numbers directly from the establishments, and response is mandatory. Multiple economists from different BLS programs said QCEW was the way to go.

We downloaded the 2003 to 2012 annual average .csv files from [here](http://www.bls.gov/cew/datatoc.htm), and then imported each into a single annual_averages table. Initially, this gave us 36 million records, so the queries on this table were running rather slowly. But most of these records were for employment and wage data for specific counties and metro-areas, which is a level of detail we don't get in CFOI. So as we imported each year's annual average records, we deleted those at any [aggregation level](http://www.bls.gov/cew/doc/titles/agglevel/agglevel_titles.htm) we can't use.

We also downloaded and imported all five of QCEW's look-up tables: [Industries](http://www.bls.gov/cew/doc/titles/industry/industry_titles.htm), [Areas](http://www.bls.gov/cew/doc/titles/area/area_titles.htm), [Ownerships](http://www.bls.gov/cew/doc/titles/ownership/ownership_titles.htm), [Size Classes](http://www.bls.gov/cew/doc/titles/size/size_titles.htm) and [Aggregation Levels](http://www.bls.gov/cew/doc/titles/agglevel/agglevel_titles.htm).

The [get_cew_data.py](https://github.com/gordonje/deadly_work/blob/master/1_db_build/get_cew_data.py) script in this repo will import the CEW into any database on your local server. This script won't download the files for you. Rather, you'll need to download, unzip and store them in 'deadly_work/1_db_build/data/'. Again, you must have the [dependencies](https://github.com/gordonje/deadly_work#dependencies) installed, and you'll be prompted for the database's name, your PostgreSQL username and password.

Joining Fatality and Employment Data
------------------------------------

We started with the relevant look-up tables.

First, we [joined the areas](https://github.com/gordonje/deadly_work/blob/master/1_db_build/sql/join_areas.sql) into a single table that contains a record for each state and one for the national level. Note that, in the case of New York State, the CFOI area_code labeled 'New York State (except NYC)' lines up to the CEW area_fips labeled 'New York -- Statewide', which does include NYC. A CFOI economist that the more appropriate alignment is with area_code 'S69', labeled 'New York State and New York City'.

We also add state abbrevations from a [translator table](https://github.com/gordonje/deadly_work/blob/master/1_db_build/state_fips_to_abbrv.txt) in this repo. This will be helpful when joining to other data sources down the road.

Then, we [joined industries](https://github.com/gordonje/deadly_work/blob/master/1_db_build/sql/join_industries.sql) into a single table that contains only the industries included in both CFOI and CEW. Note that industry names in fi and fw use different character casing (e.g., 'Specialty trade contractors' versus 'Specialty Trade Contractors'), so we use the INITCAP() function to make PostgreSQL ignore this these distinctions.

The industry codes are nested, with very specific industries (e.g., "Natural gas liquid extraction" coded "211112") fitting under more general ones (e.g., "Oil and gas extraction" coded "211XXX"). The CFOI and QCEW industries starte to intersect at the 3-digit NAICS level.

(More here about industries that are excluded).


We then used the aligned areas and industries to [join employee and fatalities counts](https://github.com/gordonje/deadly_work/blob/master/1_db_build/sql/join_cfoi_to_cew.sql) into a single table. A couple of things to note about this query:

*	Since there are going to be years in which no one died in a particular state and industry (or there were too few to disclose), and we need to include the employment numbers for those year. Therefore, it's important to select the employment numbers first then [left join](https://github.com/gordonje/deadly_work/blob/master/1_db_build/sql/join_cfoi_to_cew.sql#L50) to the fatality records.

*   In QCEW, when you drill down to the industry-level, you'll find that the numbers are also broken down by sector (aka, [ownerships](http://www.bls.gov/cew/doc/titles/ownership/ownership_titles.htm)). So there's isn't one record that tells you how many electrical contractors were working in 2012 (either at the national or the state-level). Instead, we [sum the numbers for the non-overlapping sectors](https://github.com/gordonje/deadly_work/blob/master/1_db_build/sql/join_cfoi_to_cew.sql#L34) (i.e., own_codes 1 through 5).

We also add the to areas table the [count of industries](https://github.com/gordonje/deadly_work/blob/master/1_db_build/sql/count_all_industries_for_states.sql) in each area and the [count of industries with fatalities](https://github.com/gordonje/deadly_work/blob/master/1_db_build/sql/count_fatal_industries_for_states.sql) in each area.

We also add the to industries table the [count of states](https://github.com/gordonje/deadly_work/blob/master/1_db_build/sql/count_all_states_for_industries.sql) with workers in each industry and the [count of states with fatalities](https://github.com/gordonje/deadly_work/blob/master/1_db_build/sql/count_fatal_states_for_industries.sql) in each industry.

The [join_cfoi_to_cew.py](https://github.com/gordonje/deadly_work/blob/master/1_db_build/join_cfoi_to_cew.py) script will create and populate the joined tables for you and add the columns mentioned above.