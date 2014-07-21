import getpass
import psycopg2
import os

db = raw_input("Enter name of target database):")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}


# print "Creating table..."

# with psycopg2.connect(conn_string) as conn:
# 	with conn.cursor() as cur:
# 		cur.execute('''CREATE TABLE cew.annual_averages_2012 (
# 						  area_fips varchar(5) 
# 						, own_code	numeric 
# 						, industry_code varchar(6) 
# 						, agglvl_code numeric 
# 						, size_code numeric 
# 						, year numeric 
# 						, qtr varchar(1) 
# 						, disclosure_code varchar(1) 
# 						--, area_title varchar(80) 
# 						--, own_title	varchar(80) 
# 						--, industry_title varchar(80) 
# 						--, agglvl_title varchar(80) 
# 						--, size_title varchar(80) 
# 						, annual_avg_estabs_count numeric 
# 						, annual_avg_emplvl	 numeric 
# 						, total_annual_wages numeric 
# 						, taxable_annual_wages numeric 
# 						, annual_contributions numeric 
# 						, annual_avg_wkly_wage numeric
# 						, avg_annual_pay numeric 
# 					);''')

# print "Importing..."

# in_file = os.getcwd() + '/2012.annual.singlefile.csv'

# with psycopg2.connect(conn_string) as conn:
# 	with conn.cursor() as cur:
# 		cur.execute('''COPY cew.annual_averages_2012 FROM %s DELIMITER ',' CSV HEADER;''', (in_file, ))


# print "Deleting unwanted records..."

# with psycopg2.connect(conn_string) as conn:
# 	with conn.cursor() as cur:
# 		cur.execute('''DELETE 
# 						FROM cew.annual_averages_2012 
# 						WHERE (agglvl_code >= 30 AND agglvl_code <= 49)
# 						OR agglvl_code >= 70;''')


print "Indexing..."

# with psycopg2.connect(conn_string) as conn:
# 	with conn.cursor() as cur:
# 		print 'Indexing on area_fips...'

# 		cur.execute('''CREATE INDEX annual_averages_2012_area_ind ON cew.annual_averages_2012 (area_fips);''')

with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		print 'Indexing on industry_code...'
		
		cur.execute('''CREATE INDEX annual_average_2012_industry_ind ON cew.annual_averages_2012 (industry_code);''')
		
with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		print 'Indexing on year...'

		cur.execute('''CREATE INDEX annual_average_2012_year_ind ON cew.annual_averages_2012 (year);''')
		
with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		print 'Indexing on own_code...'

		cur.execute('''CREATE INDEX annual_average_2012_own_ind ON cew.annual_averages_2012 (own_code);''')
		
with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		print 'Indexing on area_fips and industry_code...'
		
		cur.execute('''CREATE INDEX annual_averages_2012_area_industry_ind ON cew.annual_averages_2012 (area_fips, industry_code);''')
		
with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		print 'Indexing on area_fips, industry_code and year...'
		
		cur.execute('''CREATE INDEX annual_average_2012_area_industry_year_ind ON cew.annual_averages_2012 (area_fips, industry_code, year);''')
		
with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		print 'Indexing on establishment counts...'

		cur.execute('''CREATE INDEX annual_average_2012_estabs_ind ON cew.annual_averages_2012 (annual_avg_estabs_count);''')
		
with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		print 'Indexing on employment level...'

		cur.execute('''CREATE INDEX annual_average_2012_emplvl_ind ON cew.annual_averages_2012 (annual_avg_emplvl);''')
