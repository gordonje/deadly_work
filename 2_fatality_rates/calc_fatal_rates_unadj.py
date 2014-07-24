import psycopg2
import getpass

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


db = raw_input("Enter name of target database:")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}



# calculating state-level numbers

print "Summing fatalites for each area..."

if has_column(conn_string, 'public', 'areas', 'fatals_total') == False:
	
	print '    Add column...'

	execute_sql(conn_string, '''ALTER TABLE areas ADD COLUMN fatals_total numeric;''')

execute_sql(conn_string, open("sql/add_areas_fatals_total.sql", "r").read())


print "Summing employees for each area..."

if has_column(conn_string, 'public', 'areas', 'emplvl_total') == False:
	
	print '    Add column...'

	execute_sql(conn_string, '''ALTER TABLE areas ADD COLUMN emplvl_total numeric;''')

execute_sql(conn_string, open("sql/add_areas_emps_total.sql", "r").read())


print "Calculating unadjusted fatality rate for each area..."

if has_column(conn_string, 'public', 'areas', 'fatals_per_100k_unadj') == False:
	
	print '    Add column...'

	execute_sql(conn_string, '''ALTER TABLE areas ADD COLUMN fatals_per_100k_unadj numeric;''')

execute_sql(conn_string, open("sql/calc_areas_unadj_fatal_rate.sql", "r").read())



# calculating industry-level numbers

print "Summing fatalities for each industry..."

if has_column(conn_string, 'public', 'industries', 'fatals_total') == False:
	
	print '    Add column...'

	execute_sql(conn_string, '''ALTER TABLE industries ADD COLUMN fatals_total numeric;''')

execute_sql(conn_string, open("sql/add_industries_fatals_total.sql", "r").read())


print "Summing employees for each industry..."

if has_column(conn_string, 'public', 'industries', 'emplvl_total') == False:
	
	print '    Add column...'

	execute_sql(conn_string, '''ALTER TABLE industries ADD COLUMN emplvl_total numeric;''')

execute_sql(conn_string, open("sql/add_industries_emps_total.sql", "r").read())


print "Calculating national fatality rate for each industry..."

if has_column(conn_string, 'public', 'industries', 'fatals_per_100k') == False:
	
	print '    Add column...'

	execute_sql(conn_string, '''ALTER TABLE industries ADD COLUMN fatals_per_100k numeric;''')

execute_sql(conn_string, open("sql/calc_industry_national_rates.sql", "r").read())



# calculating state-industry level numbers

if has_table(conn_string, 'public', 'states_industries') == False:
	
	print 'Calculating state-industry rates...'

	execute_sql(conn_string, open("sql/create_states_industries.sql", "r").read())


print 'Ranking states within industries by fatality rate...'

if has_column(conn_string, 'public', 'states_industries', 'state_rank') == False:
	
	print '    Adding column...'

	execute_sql(conn_string, 'ALTER TABLE states_industries ADD COLUMN state_rank int;')

execute_sql(conn_string, open("sql/rank_states_in_industries.sql", "r").read())


print 'Counting the number of industries in which each state has worst fatality rate...'

if has_column(conn_string, 'public', 'areas', 'top_1_count') == False:
	
	print '    Adding column...'

	execute_sql(conn_string, 'ALTER TABLE states_industries ADD COLUMN top_1_count int;')

execute_sql(conn_string, open("sql/count_areas_top1s.sql", "r").read())


print 'Counting the number of industries in which each state has one of the five worst fatality rates...'

if has_column(conn_string, 'public', 'areas', 'top_5_count') == False:
	
	print '    Adding column...'

	execute_sql(conn_string, 'ALTER TABLE states_industries ADD COLUMN top_5_count int;')

execute_sql(conn_string, open("sql/count_areas_top5s.sql", "r").read())


print "Finished"

