import psycopg2
import getpass
import os

def execute_sql(conn_string, sql_string):

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(sql_string)

	cur.close()
	conn.close()


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

	cur.close()
	conn.close()


def has_column(conn_string, schema_name, table_name, column_name):
	query = '''SELECT * FROM information_schema.columns WHERE table_schema = %s AND table_name = %s AND column_name = %s'''
	data = (schema_name, table_name, column_name)

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(query, data)
			has_column = cur.fetchone()

	if has_column == None:
		return False
	else:
		return True

	cur.close()
	conn.close()


db = raw_input("Enter name of target database):")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}


# dealing with areas

if has_table(conn_string, 'public', 'areas') == False:
	
	print 'Joining areas...'

	execute_sql(conn_string, open("sql/join_areas.sql", "r").read())


if has_column(conn_string, 'public', 'areas', 'abbrv') == False:

	print 'Adding state abbreviations...'

	if has_table(conn_string, 'public', 'state_fips_to_abbrv') == False:

		'    Importing from text file...'

		execute_sql(conn_string, '''CREATE TABLE state_fips_to_abbrv (
										  state varchar(30)
										, abbrv varchar(3)
										, FIPS varchar(3)
									);'''
					)

				in_file = os.getcwd() + '/state_fips_to_abbrv.txt'

		execute_sql(conn_string, '''COPY state_fips_to_abbrv FROM %s WITH (DELIMITER E'\t');''', (in_file, ))

	execute_sql(conn_string, 'ALTER TABLE areas ADD COLUMN abbrv varchar(3);')

	execute_sql(conn_string, open("sql/add_state_abbrvs.sql", "r").read())



# dealing with industries

if has_table(conn_string, 'public', 'industries') == False:

	print 'Joining industries...'

	execute_sql(conn_string, open("sql/join_industries.sql", "r").read())

	print "    Adding translated industries..."

	in_file = os.getcwd() + '/high_level_industries_translator.csv'

	execute_sql(conn_string, "COPY public.industries FROM %s CSV HEADER;", (in_file, ))



# dealing with annual numbers

if has_table(conn_string, 'public', 'states_industries_years') == False:

	print 'Joining annual fatality counts and annual employee levels...'

	execute_sql(conn_string, open("sql/join_cfoi_to_cew.sql", "r").read())



# adding counts 

print "Counting industries for each area..."

if has_column(conn_string, 'public', 'areas', 'all_industries_count') == False:
	
	print '    Add column...'

	execute_sql(conn_string, '''ALTER TABLE areas ADD COLUMN all_industries_count numeric;''')

execute_sql(conn_string, open("sql/count_all_industries_for_states.sql", "r").read())


print "Counting deadly industries for each area..."

if has_column(conn_string, 'public', 'areas', 'fatal_industries_count') == False:
	
	print '    Add column...'

	execute_sql(conn_string, '''ALTER TABLE areas ADD COLUMN fatal_industries_count numeric;''')

execute_sql(conn_string, open("sql/count_fatal_industries_for_states.sql", "r").read())


print "Counting states where employees work in each industry..."

if has_column(conn_string, 'public', 'industries', 'all_states_count') == False:
	
	print '    Add column...'

	execute_sql(conn_string, '''ALTER TABLE industries ADD COLUMN all_states_count numeric;''')

execute_sql(conn_string, open("sql/count_all_states_for_industries.sql", "r").read())


print "Counting states where employees have died in each industry..."

if has_column(conn_string, 'public', 'industries', 'fatal_states_count') == False:
	
	print '    Add column...'

	execute_sql(conn_string, '''ALTER TABLE industries ADD COLUMN fatal_states_count numeric;''')

execute_sql(conn_string, open("sql/count_fatal_states_for_industries.sql", "r").read())



print "Finished"