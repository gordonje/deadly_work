import getpass
import psycopg2
import os

def has_table(conn_string, schema_name, table_name):
	query = 'SELECT * FROM information_schema.tables WHERE table_schema = %s AND table_name = %s'
	data = (schema_name, table_name)

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(query, data)
			has_table = cur.fetchone()

	if has_table == None:
		return False
	else:
		return True


db = raw_input("Enter name of target database):")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}


# Make the cew schema if it doesn't already exist
with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute('''CREATE SCHEMA IF NOT EXISTS cew;''')


# test to see if we have an annual_averages table. If not, make one, import the data for it, then index it.

if has_table(conn_string, 'cew', 'annual_averages') == False:

	print "Creating annual averages table..."

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute('''CREATE TABLE cew.annual_averages (
							  area_fips varchar(5) 
							, own_code	numeric 
							, industry_code varchar(6) 
							, agglvl_code numeric 
							, size_code numeric 
							, year numeric 
							, qtr varchar(1) 
							, disclosure_code varchar(1) 
							--, area_title varchar(80) 
							--, own_title	varchar(80) 
							--, industry_title varchar(80) 
							--, agglvl_title varchar(80) 
							--, size_title varchar(80) 
							, annual_avg_estabs_count numeric 
							, annual_avg_emplvl	 numeric 
							, total_annual_wages numeric 
							, taxable_annual_wages numeric 
							, annual_contributions numeric 
							, annual_avg_wkly_wage numeric
							, avg_annual_pay numeric 
						);''')

	# loop over each csv file, copying the contents to the annual_averages table

	print "Importing annual averages files..."

	for i in range(2003, 2013):

		in_file = os.getcwd() + '/' + str(i) + '.annual.singlefile.csv'

		with psycopg2.connect(conn_string) as conn:
			with conn.cursor() as cur:
				cur.execute('''COPY cew.annual_averages FROM %s DELIMITER ',' CSV HEADER;''', (in_file, ))

				cur.execute('''DELETE 
								FROM cew.annual_averages 
								WHERE agglvl_code NOT IN (14, 15, 16, 17, 18,
															54, 55, 56, 57, 58);''')

		print 'Finished ' + str(i) + '...'

	# then index the annual_averages table.

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			print 'Indexing on area_fips...'

			cur.execute('''CREATE INDEX annual_averages_area_ind ON cew.annual_averages (area_fips);''')

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			print 'Indexing on industry_code...'
			
			cur.execute('''CREATE INDEX annual_average_industry_ind ON cew.annual_averages (industry_code);''')
			
	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			print 'Indexing on year...'

			cur.execute('''CREATE INDEX annual_average_year_ind ON cew.annual_averages (year);''')
			
	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			print 'Indexing on own_code...'

			cur.execute('''CREATE INDEX annual_average_own_ind ON cew.annual_averages (own_code);''')
			
	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			print 'Indexing on area_fips and industry_code...'
			
			cur.execute('''CREATE INDEX annual_averages_area_industry_ind ON cew.annual_averages (area_fips, industry_code);''')
			
	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			print 'Indexing on area_fips, industry_code and year...'
			
			cur.execute('''CREATE INDEX annual_average_area_industry_year_ind ON cew.annual_averages (area_fips, industry_code, year);''')
			
	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			print 'Indexing on establishment counts...'

			cur.execute('''CREATE INDEX annual_average_estabs_ind ON cew.annual_averages (annual_avg_estabs_count);''')
			
	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			print 'Indexing on employment level...'

			cur.execute('''CREATE INDEX annual_average_emplvl_ind ON cew.annual_averages (annual_avg_emplvl);''')

# test to see if we have an industries table. if not, make one and get the data for it, then index it.

if has_table(conn_string, 'cew', 'industries') == False:

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			print "Creating industries table..."

			cur.execute('''CREATE TABLE cew.industries (
		                    code varchar(6) PRIMARY KEY,
		                    title varchar(80)
		                    );''')

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			in_file = os.getcwd() + '/' + 'industry_titles.csv' 
			cur.execute('''COPY cew.industries FROM %s DELIMITER ',' CSV HEADER;''', (in_file, ))	

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:cur.execute('''CREATE INDEX industries_code_ind ON cew.industries (code);''')

# test to see if we have an areas table. if not, make one and get the data for it, then index it.

if has_table(conn_string, 'cew', 'areas') == False:

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:	
			print "Creating areas table..."

			cur.execute('''CREATE TABLE cew.areas (
		                    code varchar(5) PRIMARY KEY,
		                    title varchar(80)
		                    );''')

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:		
			in_file = os.getcwd() + '/' + 'area_titles.csv' 
			cur.execute('''COPY cew.areas FROM %s DELIMITER ',' CSV HEADER;''', (in_file, ))	
	
	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:	
			cur.execute('''CREATE INDEX areas_code_ind ON cew.areas (code);''')


# test to see if we have an ownership table. if not, make one and get the data for it, then index it.

if has_table(conn_string, 'cew', 'ownerships') == False:

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:

			print "Creating ownerships table..."

			cur.execute('''CREATE TABLE cew.ownerships (
		                    code varchar(1) PRIMARY KEY,
		                    title varchar(80)
		                );''')

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:	
			in_file = os.getcwd() + '/' + 'ownership_titles.csv' 
			cur.execute('''COPY cew.ownerships FROM %s DELIMITER ',' CSV HEADER;''', (in_file, ))	

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute('''CREATE INDEX ownerships_code_ind ON cew.ownerships (code);''')

# test to see if we have an size classes table. if not, make one and get the data for it, then index it.

if has_table(conn_string, 'cew', 'sizes') == False:

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:

			print "Creating sizes table..."

			cur.execute('''CREATE TABLE cew.sizes (
            		        code varchar(1) PRIMARY KEY,
                    		title varchar(80)
                    	);''')

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:	
			in_file = os.getcwd() + '/' + 'size_titles.csv' 
			cur.execute('''COPY cew.sizes FROM %s DELIMITER ',' CSV HEADER;''', (in_file, ))	

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute('''CREATE INDEX size_code_ind ON cew.sizes (code);''')
	

# test to see if we have an aggregation levels table. if not, make one and get the data for it, then index it.

if has_table(conn_string, 'cew', 'agg_levels') == False:

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			print "Creating agg_levels table..."

			cur.execute('''CREATE TABLE cew.agg_levels (
		                    code int4 PRIMARY KEY,
		                    title varchar(80)
		                    );''')
	

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:	
			in_file = os.getcwd() + '/' + 'agglevel_titles.csv' 
			cur.execute('''COPY cew.agg_levels FROM %s DELIMITER ',' CSV HEADER;''', (in_file, ))	


	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:	
			cur.execute('''CREATE INDEX agg_levels_code_ind ON cew.agg_levels (code);''')


cur.close()
conn.close()

print "Finished."