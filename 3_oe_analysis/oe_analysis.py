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



print "Calculating expected fatalities in each industry for each state..."

if has_column(conn_string, 'public', 'states_industries', 'expect_fatals') == False:
	
	print '    Add column...'

	execute_sql(conn_string, '''ALTER TABLE states_industries ADD COLUMN expect_fatals numeric;''')

execute_sql(conn_string, open("sql/calc_expected_fatals.sql", "r").read())



print "Calculating state-industry residuals..."

if has_column(conn_string, 'public', 'states_industries', 'residual') == False:
	
	print '    Add column...'

	execute_sql(conn_string, '''ALTER TABLE states_industries ADD COLUMN residual numeric;''')

execute_sql(conn_string, open("sql/calc_states_industries_res.sql", "r").read())


# getting results for NAICS sectors

## agri

print "Getting state results for NAICS sectors (including agriculture)..."

if has_table(conn_string, 'public', 'states_naics2_w_agri') == False:
	
	print '    Adding table...'

	execute_sql(conn_string, open("sql/create_states_naics2_w_agri.sql", "r").read())


print "    Calculating risk-adjusted fatality rate for each state..."

if has_column(conn_string, 'public', 'states_naics2_w_agri', 'fatals_per_100k_adj') == False:
	
	print '        Add column...'

	execute_sql(conn_string, '''ALTER TABLE states_naics2_w_agri ADD COLUMN fatals_per_100k_adj numeric;''')

execute_sql(conn_string, open("sql/calc_states_naics2_w_agri_adj_rate.sql", "r").read())


## non-agri

print "Getting state results for NAICS sectors (minus agriculture)..."

if has_table(conn_string, 'public', 'states_naics2_no_agri') == False:
	
	print '    Adding table...'

	execute_sql(conn_string, open("sql/create_states_naics2_no_agri.sql", "r").read())


print "    Calculating state residuals for all non-agricultural industries..."

if has_column(conn_string, 'public', 'states_naics2_no_agri', 'residual') == False:
	
	print '        Add column...'

	execute_sql(conn_string, '''ALTER TABLE states_naics2_no_agri ADD COLUMN residual numeric;''')

execute_sql(conn_string, open("sql/calc_states_naics2_no_agri_res.sql", "r").read())


print "    Calculating risk-adjusted fatality rate for each state..."

if has_column(conn_string, 'public', 'states_naics2_no_agri', 'fatals_per_100k_adj') == False:
	
	print '        Add column...'

	execute_sql(conn_string, '''ALTER TABLE states_naics2_no_agri ADD COLUMN fatals_per_100k_adj numeric;''')

execute_sql(conn_string, open("sql/calc_states_naics2_no_agri_adj_rate.sql", "r").read())




# getting results for 3 digit NAICS industries

## agri

print "Getting state results for 3-digit NAICS industries (including agriculture)..."

if has_table(conn_string, 'public', 'states_naics3_w_agri') == False:
	
	print '    Adding table...'

	execute_sql(conn_string, open("sql/create_states_naics3_w_agri.sql", "r").read())


print "    Calculating risk-adjusted fatality rate for each state..."

if has_column(conn_string, 'public', 'states_naics3_w_agri', 'fatals_per_100k_adj') == False:
	
	print '        Add column...'

	execute_sql(conn_string, '''ALTER TABLE states_naics3_w_agri ADD COLUMN fatals_per_100k_adj numeric;''')

execute_sql(conn_string, open("sql/calc_states_naics3_w_agri_adj_rate.sql", "r").read())


## non-agri

print "Getting state results for 3-digit NAICS industries (minus agriculture)..."

if has_table(conn_string, 'public', 'states_naics3_no_agri') == False:
	
	print '    Adding table...'

	execute_sql(conn_string, open("sql/create_states_naics3_no_agri.sql", "r").read())


print "    Calculating state residuals for all non-agricultural industries..."

if has_column(conn_string, 'public', 'states_naics3_no_agri', 'residual') == False:
	
	print '        Add column...'

	execute_sql(conn_string, '''ALTER TABLE states_naics3_no_agri ADD COLUMN residual numeric;''')

execute_sql(conn_string, open("sql/calc_states_naics3_no_agri_res.sql", "r").read())


print "    Calculating risk-adjusted fatality rate for each state..."

if has_column(conn_string, 'public', 'states_naics3_no_agri', 'fatals_per_100k_adj') == False:
	
	print '        Add column...'

	execute_sql(conn_string, '''ALTER TABLE states_naics3_no_agri ADD COLUMN fatals_per_100k_adj numeric;''')

execute_sql(conn_string, open("sql/calc_states_naics3_no_agri_adj_rate.sql", "r").read())


print "Finished"
