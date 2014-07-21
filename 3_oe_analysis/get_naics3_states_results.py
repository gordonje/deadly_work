import psycopg2
import getpass

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

db = raw_input("Enter name of target database:")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}



print "Summing expected fatals for each state..."

if has_column(conn_string, 'public', 'states_naics_3', 'expect_fatals_sum') == False:
	
	print '    Add column...'

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute('''ALTER TABLE states_naics_3 ADD COLUMN expect_fatals_sum numeric;''')

with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute(open("sql/sum_states_expect_fatals.sql", "r").read())



print "Calculating residual for each state..."

if has_column(conn_string, 'public', 'states_naics_3', 'residual') == False:
	
	print '    Add column...'

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute('''ALTER TABLE states_naics_3 ADD COLUMN residual numeric;''')

with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute(open("sql/calc_state_residuals.sql", "r").read())



print "Calculating adjusted fatality rate for each state..."

if has_column(conn_string, 'public', 'states_naics_3', 'residual') == False:
	
	print '    Add column...'

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute('''ALTER TABLE states_naics_3 ADD COLUMN fatals_per_100k_adj numeric;''')

with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute(open("sql/calc_states_adj_fatal_rate.sql", "r").read())



print "Calculating percentage of risk captured in each state..."

if has_column(conn_string, 'public', 'states_naics_3', 'pct_risk_capd') == False:
	
	print '    Add column...'

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute('''ALTER TABLE states_naics_3 ADD COLUMN pct_risk_capd numeric;''')

with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute(open("sql/calc_pct_states_risk_capd.sql", "r").read())


cur.close()
conn.close()

print "Finished"