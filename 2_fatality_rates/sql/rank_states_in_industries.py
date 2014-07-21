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


db = raw_input("Enter name of target database):")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}

if has_table(conn_string, 'public', 'states_naics_3') == False:
	
	print 'Creating states NAICS 3 table...'

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(open("sql/create_states_naics_3.sql", "r").read())


print 'Counting NAICS 3 industries for state...'

if has_column(conn_string, 'public', 'states_naics_3', 'industries_count') == False:
	
	print '    Adding column...'

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute('ALTER TABLE states_naics_3 ADD COLUMN industries_count numeric;')

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(open("sql/count_inds_for_naics3_states.sql", "r").read())

cur.close()
conn.close()

print "Finished"

